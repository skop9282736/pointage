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
}
new Vue({
	el: '#root',
	data:{
		salaries: [],
		salary: {
			id_salary_finger: '',
			group_salary: '',
			first_name: '',
			last_name: '',
			date_joined: '',
		},
		salaryId: '',
		errors: new Errors()

	},
	mounted(){
		axios.get('/employees/salaries')
		.then(response => this.salaries = response.data)
	},
	methods: {
		addSalary(event) {
			axios.post('/employees/salaries/', this.$data.salary)
			  .then(response => this.salaries.unshift(this.salary) )
			  .then(response => this.salary = {})
			  .then(function (response) {
				swal("Employé ajouté avec succès!");
			  })
			  .catch(errors => this.errors.record(errors.response.data))
		},
		showAddSalary(){
			this.salary = {}
		},
		getSalaryId(salary){
			axios.get('/employees/salaries/getid/'+salary.id_salary_finger)
			.then(response => this.salaryId = response.data)
		},
		showEditSalary(salary){
			this.salary = salary
			this.getSalaryId(salary)
		},
		EditSalary(event) {
			axios.put('/employees/salaries/'+this.salaryId+'/', this.$data.salary)
			.then(function (response) {
			    $.alert({
				    title: 'Succès!',
				    content: 'employé édité avec succès!',
				});
			  })
		},
		deleteSalary(salary, index){
			this.salary = salary
			this.getSalaryId(salary)
			swal({
			  title: "Êtes-vous sûr?",
			  text: "Une fois supprimé, vous ne serez pas en mesure de récupérer cet enregistrement!",
			  icon: "warning",
			  buttons: true,
			  dangerMode: true,
			})
			.then((willDelete) => {
			  if (willDelete) {
			  	axios.delete('/employees/salaries/'+this.salaryId)
			  	this.$delete(this.salaries, index)
			    swal("employé supprimé.", {
			      icon: "success",
			    });
			  }
			});
		}

	}
})