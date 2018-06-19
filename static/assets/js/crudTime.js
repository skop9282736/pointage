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
	el: '#rootTime',
	data:{
            timeEnter:{
								id:'',
                group:'',
                group_name:'',
                time_enter_morning:'',
                time_out_morning:'',
                time_enter_evening:'',
                time_out_evening:'',
                full_time:false,
			},
            times:[],
            groups:[],
			errors: new Errors()
	},
	mounted(){
		axios.get('/pointage/times/')
		.then(response => this.times = response.data)
        axios.get('/pointage/groups/')
		.then(response => {
			this.groups = response.data;
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
		getSalaryName(groupId){
			var name = ''
			// console.log(salaryId)
			if(!groupId) return name;
			this.groups.filter((g) => {
					if(groupId == g.id){
						name = g.name
						
					}
			})
			return name
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
		      .then(response => this.times = response.data)

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

    },
    

})