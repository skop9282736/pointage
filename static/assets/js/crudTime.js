axios.defaults.xsrfHeaderName = "X-CSRFToken";

class Errors {
	constructor(){
		this.errors = {};
	}
	get(field){
		if (this.errors[field]){
			return this.errors[field][0];
		}
	}
	record(errors){
		this.errors = errors;
	}

	clear(field){
		delete this.errors[field]
	}

	has(field){
		return this.errors.hasOwnProprety;
	}
}


new Vue({
	el: '#rootTime',
	data:{		
						
            timeEnter:{
				id:'',
                group:'',
                time_enter_morning:'00:00',
                time_out_morning:'00:00',
                time_enter_evening:'00:00',
                time_out_evening:'00:00',
                full_time:true,
			},
			times:[],

			breack:{
					id:'',
					salary:'',
					start:'',
					end:'',
			},
			groups:[],
			salaries:[],
			Breacks:[],
			holiday:{
					holiday_name:'',
					start:'',
					end: ''
			},
			holidays:[],
			errors: new Errors(),
	},
	mounted(){
				axios.get('/pointage/times/')
				.then(response => this.times = response.data)
				axios.get('/pointage/groups/')
				.then(response => {
					this.groups = response.data;
				})
				axios.get('/pointage/Breacks/')
				.then(response => {
					this.Breacks = response.data;
				})
				axios.get('/pointage/salaries/')
				.then(response => {
					this.salaries = response.data;
				})

				axios.get('/pointage/holidays/')
				.then(response => {
					this.holidays = response.data;
				})

				
		
    },
    methods: {
		isPermanence(time)
		{
			if (time.full_time == true)
			{
				return "permanence"
			}
			else{
				return "non permanence"
			}
			

		},

		getGroupName(groupId){
			var name = ''
			if(!groupId) return name;
			this.groups.filter((g) => {
					if(groupId == g.id){
						name = g.name
						
					}
			})
			return name
		},

		showAddTimeEnter(){
			this.timeEnter = {};
			this.timeEnter.time_enter_morning='00:00';
			this.timeEnter.time_out_morning='00:00';
			this.timeEnter.time_enter_evening='00:00';
			this.timeEnter.time_out_evening='00:00';
		},

		addTimeEnter(event) {
			axios.post('/pointage/times/', this.$data.timeEnter)
			.then(response => this.times.unshift(this.timeEnter) )
			.then(response => this.timeEnter = {})
			.then(function (response) {
			swal("Employé ajouté avec succès!");
			})
			.catch(errors => this.errors.record(errors.response.data))
			this.modalShown = false

			axios.get('/pointage/times')
				.then(response => this.times = response.data);
				this.showAddTimeEnter()
		},
		

		showEditTime(time){
			this.timeEnter = time
			
		},

		EditTime(event) {
			axios.put('/pointage/times/'+this.timeEnter.id+'/', this.$data.timeEnter)
			.then(function (response) {
			    $.alert({
				    title: 'Succès!',
				    content: 'employé édité avec succès!',
				});
				})
				.catch(errors => this.errors.record(errors.response.data))
				this.modalShown = false
		},
		
		deleteTime(time, index){
			this.timeEnter = time
			swal({
			  title: "Êtes-vous sûr?",
			  text: "Une fois supprimé, vous ne serez pas en mesure de récupérer cet enregistrement!",
			  icon: "warning",
			  buttons: true,
			  dangerMode: true,
			})
			.then((willDelete) => {
			  if (willDelete) {
			  	axios.delete('/pointage/times/'+this.timeEnter.id)
			  	this.$delete(this.times, index)
			    swal("employé supprimé.", {
			      icon: "success",
			    });
			  }
			});
		},

		// ---------------------------------Function breack--------------
		addBreak(event) {
			axios.post('/pointage/Breacks/', this.$data.breack)
			.then(response => this.Breacks.unshift(this.breack) )
			.then(response => this.breack = {})
			.then(function (response) {
			swal("Employé ajouté avec succès!");
			})
			.catch(errors => this.errors.record(errors.response.data))
			this.modalShown = false
			axios.get('/pointage/Breacks')
				.then(response => this.Breacks = response.data)

		},

		showAddBreak(){
			this.breack = {}	;
			this.errors.clear('end') ;
			this.errors.clear('start');
		},

		getSalaryName(salaryId){
			var name = 'aa'
			if(!salaryId) return name;
			this.salaries.filter((s) => {
					if(salaryId == s.id){
						name = s.first_name
						
					}
			})
			return name
		},

		showEditeBeak(breack){
			this.breack= breack;
			this.errors.clear('end') ;
			this.errors.clear('start');
		},
		EditBreak(event) {
			axios.put('/pointage/Breacks/'+this.breack.id+'/', this.$data.breack)
			.then(function (response) {
			    $.alert({
				    title: 'Succès!',
				    content: 'Break édité avec succès!',
				});
				})
				.catch(errors => this.errors.record(errors.response.data))
				this.modalShown = false
		},

		deleteBreak(breack,index){
			this.breack = breack
			swal({
			  title: "Êtes-vous sûr?",
			  text: "Une fois supprimé, vous ne serez pas en mesure de récupérer cet enregistrement!",
			  icon: "warning",
			  buttons: true,
			  dangerMode: true,
			})
			.then((willDelete) => {
			  if (willDelete) {
			  	axios.delete('/pointage/Breacks/'+this.breack.id)
			  	this.$delete(this.Breacks, index)
			    swal("Break supprimé.", {
			      icon: "success",
			    });
			  }
			});
		},	

		// ---------------------------------Function Holidays--------------
		addHoliday(event) {
			axios.post('/pointage/holidays/', this.$data.holiday)
			.then(response => this.holidays.unshift(this.holiday) )
			.then(response => this.holiday = {})
			.then(function (response) {
			swal("Holiday ajouté avec succès!");
			})
			.catch(errors => this.errors.record(errors.response.data))
			this.modalShown = false
			axios.get('/pointage/holidays')
			.then(response => this.holidays = response.data)

		},

		showAddHoliday(){
			this.holiday = {}	;
			this.errors.clear('start') ;
			this.errors.clear('end') ;
			this.errors.clear('holiday_name') ;
		},

	
		showEditeHoliday(holiday){
			this.holiday = holiday
			this.errors.clear('holiday_name') ;
			this.errors.clear('end') ;
			this.errors.clear('start');
		},
		EditHoliday(event) {
			axios.put('/pointage/holidays/'+this.holiday.id+'/', this.$data.holiday)
			.then(function (response) {
				$.alert({
					title: 'Succès!',
					content: 'Break édité avec succès!',
				});
				})
				.catch(errors => this.errors.record(errors.response.data))
				this.modalShown = false
		},
		deleteHoliday(holiday,index){
			this.holiday = holiday
			swal({
				title: "Êtes-vous sûr?",
				text: "Une fois supprimé, vous ne serez pas en mesure de récupérer cet enregistrement!",
				icon: "warning",
				buttons: true,
				dangerMode: true,
			})
			.then((willDelete) => {
				if (willDelete) {
					axios.delete('/pointage/holidays/'+this.holiday.id)
					this.$delete(this.holidays, index)
				swal("Break supprimé.", {
					icon: "success",
				});
				}
			});
		},	
},		

})