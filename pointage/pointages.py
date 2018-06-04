from django.db.models import Q
import pandas
import datetime
from django.db.models import Sum


def exists(salary, date, time, Summary):
	""" check if a summary already exists """
	lookups = Q(in_morning__exact=time) | Q(out_morning=time) | Q(in_evening=time) | Q(out_evening=time)
	summary = Summary.objects.filter(lookups).distinct().filter(salary=salary).filter(date=date)
	if summary.exists():
		return summary.first(), 1 #exists exact
	else:
		summary =Summary.objects.filter(salary=salary).filter(date=date)
		if summary.exists():
			return summary.first(), 2 # exists with date
		else:
			return (-1) # not exist



def set_time(summary, time_arg, legal_time):
	''' set time_enter time_out for a given summary '''
	if legal_time.full_time:
		if summary.in_morning is None:
			if time_arg < legal_time.time_out_morning:
				summary.in_morning = time_arg
		else:
			summary.out_morning = time_arg

	else:
		if summary.in_morning is None and time_arg < legal_time.time_out_morning:
			summary.in_morning = time_arg
		elif summary.out_morning is None and time_arg < legal_time.time_enter_evening:
			summary.out_morning = time_arg
		elif summary.in_evening is None:
			summary.in_evening = time_arg
		else:
			summary.out_evening = time_arg
	summary.save()



def set_status(summary, legal_time):
	if summary.status1 != 'break':

		if summary.in_morning is None and summary.out_morning is None:
			summary.status1 = "absent" if summary.status1 != "holiday" else "holiday"

		elif summary.in_morning is not None and summary.out_morning is None:
			summary.status1 = "incomplete" if summary.status1 != "holiday" else "holiday"
		elif summary.in_morning is None and summary.out_morning is not None:
			summary.status1 = "incomplete" if summary.status1 != "holiday" else "holiday"
		elif summary.in_morning > legal_time.time_enter_morning:
			summary.status1 = "late" if summary.status1 != "holiday" else "holiday"

			if summary.out_morning < legal_time.time_out_morning:
				summary.status1 = "late_early" if summary.status1 != "holiday" else "holiday"

		elif summary.out_morning < legal_time.time_out_morning:
			summary.status1 = "early" if summary.status1 != "holiday" else "holiday"

		else:
			summary.status1 = "in_time" if summary.status1 != "holiday" else "holiday"


		if not legal_time.full_time:
			if summary.in_evening is not None and summary.out_evening is None:
				summary.status2 = "incomplete" if summary.status1 != "holiday" else "holiday"

			elif summary.in_evening is None and summary.out_evening is None:
				summary.status2 = "absent" if summary.status1 != "holiday" else "holiday"

			elif summary.in_evening > legal_time.time_enter_evening:
				summary.status2 = "late" if summary.status1 != "holiday" else "holiday"

				if summary.out_evening < legal_time.time_out_evening:
					summary.status1 = "late_early" if summary.status1 != "holiday" else "holiday"

			elif summary.out_evening < legal_time.time_out_evening:
				summary.status2 = "early" if summary.status1 != "holiday" else "holiday"

			else:
				summary.status2 = "in_time" if summary.status1 != "holiday" else "holiday"

		summary.save()



def set_break(break_instance, Summary):
	dates 	= pandas.date_range(start=break_instance.start, end=break_instance.end)

	for date in dates:
		summary = Summary(salary=break_instance.salary, date=date, status1="break", status2="break")
		summary.save()



def set_holiday(break_instance, Summary, Salary):
	dates 	= pandas.date_range(start=break_instance.start, end=break_instance.end)
	salaries = Salary.objects.all()

	for date in dates:
		for salary in salaries:
			summary = Summary.objects.filter(salary=salary, date=date).first()
			if summary.exists():
				summary.status1 = 'holiday'
				summary.status2 = 'holiday'
				summary.save()
			else:
				summary = Summary(salary=salary, date=date, status1="holiday", status2="holiday")
				summary.save()



def set_hours(summary, legal_time):
	nb_hours = 0
	nb_minutes = 0
	if summary.in_morning is not None and summary.out_morning is not None:
		skip = ['break', 'holiday']
		if summary.status1 not in skip:
			if summary.status1 == 'late':
				nb_hours 	+= legal_time.time_out_morning.hour - summary.in_morning.hour - 1
				nb_minutes 	+= legal_time.time_out_morning.minute - summary.in_morning.minute
			elif summary.status1 == 'late_early':
				nb_hours 	+= summary.out_morning.hour - summary.in_morning.hour - 1
				nb_minutes 	+= summary.out_morning.minute - summary.in_morning.minute
			elif summary.status1 == 'early':
				nb_hours 	+= summary.out_morning.hour - legal_time.time_enter_morning.hour - 1
				nb_minutes 	+= summary.out_morning.minute - legal_time.time_enter_morning.minute
			elif summary.status1 == 'in_time':
				nb_hours 	+= legal_time.time_out_morning.hour - legal_time.time_enter_morning.hour
				# nb_minutes 	+= legal_time.time_out_morning.minute - legal_time.time_enter_morning.minute

		if summary.in_evening is not None and summary.out_evening is not None:
			if summary.status2 not in skip:
				if summary.status2 == 'late':
					nb_hours += legal_time.time_out_evening.hour - summary.in_evening.hour - 1
					nb_minutes += legal_time.time_out_evening.minute - summary.in_evening.minute
				elif summary.status2 == 'early':
					nb_hours += summary.out_evening.hour - legal_time.time_enter_evening.hour
					nb_minutes += summary.out_evening.minute - legal_time.time_enter_evening.minute
				elif summary.status2 == 'in_time':
					nb_hours += legal_time.time_out_evening.hour - legal_time.time_enter_evening.hour
					nb_minutes += legal_time.time_out_evening.minute - legal_time.time_enter_evening.minute
		if nb_minutes < 0 :
			summary.nb_hours = nb_hours
			nb_minutes = nb_minutes * (-1)
			if nb_minutes > 30:
				nb_minutes = 60 - nb_minutes
			summary.nb_minutes = nb_minutes
		else:
			if nb_minutes > 30:
				nb_minutes = 60 - nb_minutes
			summary.nb_hours = nb_hours
			summary.nb_minutes = nb_minutes
		summary.save()



def show_pointages(start, end, salary, Summary, legal_time=None):
	start_date 	 = datetime.datetime.strptime(start, "%Y-%m-%d")
	end_date 	 = datetime.datetime.strptime(end, "%Y-%m-%d")
	dates 		 = [(start_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in
                     range(0, (end_date - start_date).days + 1)]
	summaries 	 = Summary.objects.filter(date__range=(start_date, end_date)).filter(salary=salary)
	total_hours  = summaries.aggregate(Sum('nb_hours'))
	total_minutes= summaries.aggregate(Sum('nb_minutes'))
	total_absent = len(dates)

	for j,date in enumerate(dates):
		for summary in summaries:
			if summary.date == datetime.datetime.strptime(date, "%Y-%m-%d").date():
				dates[j] = summary
				total_absent -= 1

	if not legal_time.full_time:
		total_absent = total_absent * 2
		total_absent += summaries.filter(status1='absent').count()
		total_absent += summaries.filter(status2='absent').count()

	dates.append([total_hours, total_minutes, total_absent])
	return dates

# def show_pointages_all(start, end, salary, Summary, legal_time=None):
# 	start_date 	 = datetime.datetime.strptime(start, "%Y-%m-%d")
# 	end_date 	 = datetime.datetime.strptime(end, "%Y-%m-%d")
# 	dates 		 = [(start_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in
#                      range(0, (end_date - start_date).days + 1)]
# 	summaries 	 = Summary.objects.filter(date__range=(start_date, end_date))
# 	salaries	 = Salary
# 	total_hours  = summaries.aggregate(Sum('nb_hours'))
# 	total_minutes= summaries.aggregate(Sum('nb_minutes'))
# 	total_absent = len(dates)
# 	dates_to_show = dates # dates li aybano l fo9 ==> just for reading

# 	for j,date in enumerate(dates):
# 		for salary in salaries:
# 			if summary.date == datetime.datetime.strptime(date, "%Y-%m-%d").date():
# 				dates[j] = summary
# 				total_absent -= 1

# 	if not legal_time.full_time:
# 		total_absent = total_absent * 2
# 		total_absent += summaries.filter(status1='absent').count()
# 		total_absent += summaries.filter(status2='absent').count()

# 	dates.append([total_hours, total_minutes, total_absent])
# 	dates.append(dates_to_show)
# 	return dates