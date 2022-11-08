const fastapi_url = 'http://127.0.0.1:8000/'

const app = Vue.createApp({
	data() {
		return {
		    projects: [],
		    tasks: {
		        todo: [],
		        doing: [],
		        done: []
		    },
		    project_name_input_of_create_project_form: "",
		    create_task_form: {
		        project_member_username: "",
                text: "",
                deadline: "",
                status: ""
		    },
		    change_task_info_form: {
		        project_member_username: "",
                text: "",
                deadline: "",
                status: ""
		    },
            current_opened_project_id: 0,
            current_opened_task_id: 0,
		}
	},
	methods: {
		create_project_form_onsubmit(event) {
			axios.post(fastapi_url + 'create_project/', {
                name: this.project_name_input_of_create_project_form,
                admin_user_id: user_id
            }).then((response) => {
			    this.projects.push(response.data["project"])
                this.project_name_input_of_create_project_form = ""
                window.location.hash = ""
			})
		},
		create_task_form_onsubmit(event) {
		    data = Object.assign({}, {project_id: this.current_opened_project_id}, this.create_task_form)
		    axios.post(fastapi_url + 'create_task/', data)
                .then((response) => {
                    if (response.data["task"]["status"] == "To do") {
                        this.tasks["todo"].push(response.data["task"])
                    } else if (response.data["task"]["status"] == "Doing") {
                        this.tasks["doing"].push(response.data["task"])
                    } else {
                        this.tasks["done"].push(response.data["task"])
                    }
                    this.create_task_form["project_member_username"] = ""
                    this.create_task_form["text"] = ""
                    this.create_task_form["deadline"] = ""
                    this.create_task_form["status"] = ""
                    window.location.hash = ""
                })
		},
		delete_task(task_id) {
		    axios.post(fastapi_url + 'delete_task/' + task_id + '/')
                .then((response) => {
                    const task_statuses = ["todo", "doing", "done"];
                    task_statuses.forEach((task_status) => {
                        var tasks = this.tasks[task_status]
                        found = false
                        for (var i = 0; i < tasks.length; i++) {
                            if (tasks[i]["id"] == task_id) {
                                tasks.splice(i, 1)
                                found = true
                                break
                            }
                        }
                        if (found) {
                            return
                        }
                    })
                })
		},
		get_user_projects() {
		    axios(fastapi_url + 'get_user_projects/?user_id=' + user_id)
                .then((response) => {
                    this.projects = response.data["projects"]
                })
		},
		delete_project_member_from_project(project_id) {
		    axios.post(fastapi_url + 'delete_project_member_from_project/', {
                project_id: project_id,
                user_id: user_id
            }).then((response) => {
                for (var i = 0; i < this.projects.length; i++) {
                    if (this.projects[i]["id"] == project_id) {
                        this.projects.splice(i, 1)
                        break
                    }
                }
                swal("You have been deleted from the project!", {
                  icon: "success",
                });
			})
		},
		get_project_tasks() {
		    axios(fastapi_url + "get_project_tasks/?project_id=" + this.current_opened_project_id)
		        .then((response) => {
		            this.tasks = {
		                todo: [],
		                doing: [],
		                done: []
		            }
		            var tasks = response.data["tasks"]
		            for (var i = 0; i < tasks.length; i++) {
		                if (tasks[i]["status"] == "To do") {
		                    this.tasks["todo"].push(tasks[i])
		                } else if (tasks[i]["status"] == "Doing") {
		                    this.tasks["doing"].push(tasks[i])
		                } else {
		                    this.tasks["done"].push(tasks[i])
		                }
		            }
		        })
		},
		change_task_info_form_onsubmit() {
		    data = Object.assign({}, {task_id: this.current_opened_task_id}, this.change_task_info_form)
		    axios.post(fastapi_url + 'change_task_info/', data)
                .then((response) => {
                    const task_statuses = ["todo", "doing", "done"];
                    task_statuses.forEach((task_status) => {
                        var tasks = this.tasks[task_status]
                        found = false
                        for (var i = 0; i < tasks.length; i++) {
                            if (tasks[i]["id"] == this.current_opened_task_id) {
                                if (tasks[i]["status"] != response.data["task"]["status"]) {
                                    tasks.splice(i, 1)
                                    if (response.data["task"]["status"] == "To do") {
                                        this.tasks["todo"].push(response.data["task"])
                                    } else if (response.data["task"]["status"] == "Doing") {
                                        this.tasks["doing"].push(response.data["task"])
                                    } else {
                                        this.tasks["done"].push(response.data["task"])
                                    }
                                } else {
                                    tasks[i] = response.data["task"]
                                }
                                found = true
                                break
                            }
                        }
                        if (found) {
                            return
                        }
                    })
                    window.location.hash = ""
                    this.create_task_form["project_member_username"] = ""
                    this.create_task_form["text"] = ""
                    this.create_task_form["deadline"] = ""
                    this.create_task_form["status"] = ""
                })
		},
		delete_project_member_from_project_button_onclick(project_id) {
		    swal({
              title: "Are you sure?",
              text: "Once deleted, you will not be able to be a member of the project",
              icon: "warning",
              buttons: true,
              dangerMode: true,
            })
            .then((willDelete) => {
              if (willDelete) {
                this.delete_project_member_from_project(project_id)
                if (project_id == this.current_opened_project_id) {
                    document.getElementById("welcome_view").style.display = "block"
		            document.getElementById("tasks_board_view").style.display = "none"
		            this.current_opened_project_id = 0
                }
              }
            });
		},
		open_project_tasks(project_id) {
		    document.getElementById("welcome_view").style.display = "none"
		    document.getElementById("tasks_board_view").style.display = "flex"
		    this.current_opened_project_id = project_id
		    this.get_project_tasks()
		},
		delete_task_button_onclick(task_id) {
		    swal({
              title: "Are you sure?",
              text: "Once deleted, you will not be able to return the task",
              icon: "warning",
              buttons: true,
              dangerMode: true,
            })
            .then((willDelete) => {
              if (willDelete) {
                this.delete_task(task_id)
              }
            });
		},
		change_task_info_form_open(task_id) {
		    this.current_opened_task_id = task_id
		    const task_statuses = ["todo", "doing", "done"];
		    task_statuses.forEach((task_status) => {
		        var tasks = this.tasks[task_status]
		        found = false
		        for (var i = 0; i < tasks.length; i++) {
		            if (tasks[i]["id"] == task_id) {
		                this.change_task_info_form = {
                            project_member_username: tasks[i]["project_member_username"],
                            text: tasks[i]["text"],
                            deadline: tasks[i]["deadline"],
                            status: tasks[i]["status"]
                        }
                        found = true
                        break
		            }
		        }
		        if (found) {
		            return
		        }
		    })
		    window.location.hash = 'change_task_info_form'
		}
	},
	beforeMount() {
	    this.get_user_projects()
	}
})

app.config.compilerOptions.delimiters = ["${", "}"];
