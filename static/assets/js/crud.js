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
					group_salary: {id: '',name:'',},
					first_name: '',
					last_name: '',
					date_joined: '',
			},
			salaryId: '',
			groups: [],
			groupSalary: {
					id:'',
					name:'',
			},
			groupId:'',
			errors: new Errors()
	},
	mounted(){
		axios.get('/employees/salaries')
		.then(response => this.salaries = response.data)

		axios.get('/employees/groups')
		.then(response => {
			this.groups = response.data;
			// salaries.salary.group_salary_name = data.name
		})
	},
	filters:{
		group_salary_name:function(value){
				
		}
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
		},
		// ________________________________________________function crud groupe___________________________
		showAddGroup(){  
			this.groupSalary = {}
		},
		addGroup(event) {
				axios.post('/employees/groups/', this.$data.groupSalary)
			  .then(response => this.groups.unshift(this.groupSalary) )
			  .then(response => this.groupSalary = {})
			  .then(function (response) {
				swal("Employé ajouté avec succès!");
			  })
				.catch(errors => this.errors.record(errors.response.data))
				
				axios.get('/employees/groups')
				.then(response => this.groups = response.data)
		},
		getGroupId(groupSalary){
			axios.get('/employees/groups/getid/'+groupSalary.id)
			.then(response => this.groupId = response.data)
		},
		showEditGroup(group){
			this.groupSalary = group
			this.getGroupId(group)
		},
		editGroup(event){
			axios.put('/employees/groups/'+this.groupId+'/', this.$data.groupSalary)
			.then(function (response) {
			    $.alert({title: 'Succès!',content: 'groupe édité avec succès!',});
			})   
		},
		deleteGroup(group, index){
			this.group = group
			this.getGroupId(group)
			swal({
			  title: "Êtes-vous sûr?",
			  text: "Une fois supprimé, vous ne serez pas en mesure de récupérer cet enregistrement!",
			  icon: "warning",
			  buttons: true,
			  dangerMode: true,
			})
			.then((willDelete) => {
			  if (willDelete) {
			  	axios.delete('/employees/groups/'+this.groupId);
			  	this.$delete(this.groups, index);
			    swal("groupe supprimé.", {
			      icon: "success",
			    });
			  }
			});
		},
		
	
	
	}
})

