<template>
  <div>
    <ViewTitle></ViewTitle>

    <div>
      <b-card no-body>
        <b-tabs card>
          <b-tab title="All Projects" active>
            <b-card-text>
              <ProjectList :fields="fields" :items="itemsAll"></ProjectList>
            </b-card-text>
          </b-tab>
          <b-tab title="Projects of My Interest">
            <b-card-text>
              <ProjectList :fields="fields" :items="itemsInteresing"></ProjectList>
            </b-card-text>
          </b-tab>
        </b-tabs>
      </b-card>
      <br/>
      <b-card no-body>
        <b-tabs card>
          <b-tab title="My Projects" active>
            <b-card-text>
              <ProjectList :fields="fieldsMy" :items="itemsMy"></ProjectList>
            </b-card-text>
          </b-tab>
          <b-tab title="CO-PI Projects">
            <b-card-text>
              <ProjectList :fields="fields" :items="itemsMyCOPI"></ProjectList>
            </b-card-text>
          </b-tab>
        </b-tabs>
      </b-card>
    </div>
  </div>
</template>

<script>
import { getAllProject, getInterestingProjects, getMyProject, getMyCOPIProjects } from "../service/api.js";
import ProjectList from "../components/ProjectList.vue";
import ViewTitle from "../components/ViewTitle.vue";

export default {
  components: { ProjectList, ViewTitle },
  data() {
    return {
      fields: [],
      fieldsAdmin: [
        { key: "Title", label: "Title (Name of PI, University, Interest, Admin)"},
      ],
      fieldsUser: [
        { key: "Title", label: "Title (Name of PI, University, Interest)"},
      ],
      fieldsMy: [
        { key: "Title", label: "Title (Name of PI, University, Interest, Admin)"},
      ],
      itemsAll: [],
      itemsInteresing: [],
      itemsMy: [],
      itemsMyCOPI: [],

      user: localStorage.getItem("role_id")
    };
  },
  computed: {
    rows() {
      return this.items.length;
    }
  },
  methods: {
    isAdmin() {
      if (this.user == 3) {
        return true;
      }
      else
      {
        return false;
      }
    },
    getFields() {
      if (this.isAdmin())
      {
        this.fields = this.fieldsAdmin;
      }
      else
      {
        this.fields = this.fieldsUser;
      }
    }
  },
  created() {
    getAllProject().then(response => {
      const data = response.data;
      var result = data
      for (var i = result.length-1; i>=0 ; i--)
      {
        this.itemsAll.push({ project_title: data[i]['project_title'], name_of_pi: data[i]['name_of_pi'], university: data[i]['university'], researches: data[i]['researches'], id: data[i]['id'], user_id: data[i]['user_id']});
      }
    });

    getMyProject().then(response => {
      const data = response.data;
      var result = data 
      for (var i = result.length-1; i>=0 ; i--)
      {
        this.itemsMy.push({ project_title: data[i]['project_title'], name_of_pi: data[i]['name_of_pi'], university: data[i]['university'], researches: data[i]['researches'], id: data[i]['id'], user_id: data[i]['user_id']});
      }
    });

    getMyCOPIProjects().then(response => {
      const data = response.data;
      var result = data;
      for (var i = result.length-1; i>=0 ; i--)
      {
        this.itemsMyCOPI.push({ project_title: data[i]['project_title'], name_of_pi: data[i]['name_of_pi'], university: data[i]['university'], researches: data[i]['researches'], id: data[i]['id'], user_id: data[i]['user_id']});
      }
    });

    getInterestingProjects().then(response => {
      const data = response.data;
      var result = data;
      for (var i = result.length-1; i>=0 ; i--)
      {
        this.itemsInteresing.push({ project_title: data[i]['project_title'], name_of_pi: data[i]['name_of_pi'], university: data[i]['university'], researches: data[i]['researches'], id: data[i]['id'], user_id: data[i]['user_id']});
      }
    });

    this.getFields();
  }

};
</script>

<style>
.pageTitle {
  border-bottom: 2px solid #ffcf56;
  padding-bottom: 10px;
  margin-bottom: 10px;
  max-width: 10em;
  margin: auto;
  font-size: 30px;
}
</style>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>