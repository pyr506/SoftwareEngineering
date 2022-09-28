<template>
  <div>
    <b-table
      :fields="fields"
      :items="items"
      :per-page=10
      :current-page="currentPage"
    >
      <template #cell(Title)="data">
        <b-row>
          <b-col>
            <router-link :to="{name: 'ProjectPage',params:{id:data.item.id}}" class="link">{{ data.item.project_title }}</router-link>
          </b-col>
        </b-row>
        <b-row>
          <b-col class="col-12 col-sm-12 col-md-12 col-xl-12 text-nowrap">{{ data.item.name_of_pi }}</b-col>
        </b-row>
        <b-row>
          <b-col class="col-12 col-sm-12 col-md-12 col-xl-12 text-nowrap">{{ data.item.university }}</b-col>
        </b-row>
        <b-row>
          <b-col class="col-12 col-sm-12 col-md-12 col-xl-12">
            <multiselect
              v-model="data.item.researches"
              tag-placeholder="Add this as new tag"
              placeholder="Search or add a tag"
              label="name"
              track-by="id"
              :options="exp"
              :multiple="true"
              :taggable="true"
              disabled
            ></multiselect>
          </b-col>
        </b-row>
        <b-row>
          <b-col class="col-12 col-sm-12 col-md-12 col-xl-12" v-if="showControl(data.item.user_id)" >
            <button @click="gotoEditPage(data.item.id)" class="btn btn-link">Edit</button>/<button class="btn btn-link" @click="delBtn(data.item.id)">Delete</button>
          </b-col>
        </b-row>
      </template>
    </b-table>
    <b-pagination
      v-model="currentPage"
      :total-rows="rows"
      :per-page=10
      aria-controls="my-table"
      align="right"
    ></b-pagination>
  </div>
</template>

<script>
import { deleteProject } from "../service/api.js";
import Multiselect from "vue-multiselect";
export default {
  props: ["fields", "items"],
  components: {
    Multiselect
  },
  data() {
    return {
      exp: [{}],
      currentPage: 1,
      user: localStorage.getItem("role_id")
    };
  },
  computed: {
    rows() {
      return this.items.length;
    }
  },
  methods: {
    delBtn(id) {
      const msg = "Are your sure to delete the project?";
      if (confirm(msg) == true) {
        deleteProject(id)
          .then((response) => {
            if (response.status == 'error')
            {
              throw new Error(response.message);
            }
            alert("Delete success");
            window.location.reload();
          })
          .catch((error) => {
            alert("Delete error:" + error);
          });
      }
    },
    gotoEditPage(id) {
      this.$router.push(`/projects/edit/` + id);
    },
    showControl(compare_user_id) {
      return this.isAdmin() || this.isCurrentUser(compare_user_id);
    },
    isAdmin() {
      if (this.user == 3) {
        return true;
      }
      else
      {
        return false;
      }
    },
    isCurrentUser(compare_user_id) {
      console.log(localStorage.getItem("id") + ',' + compare_user_id);
      if (localStorage.getItem("id")==compare_user_id) {
        return true;
      }
      else
      {
        return false;
      }
    }
  },
  created: function() {
  }
}
</script>
