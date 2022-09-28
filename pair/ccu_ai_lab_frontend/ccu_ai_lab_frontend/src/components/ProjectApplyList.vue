<template>
  <div>
    <b-table
      :fields="fields"
      :items="items"
      :per-page=10
      :current-page="currentPage"
      thead-class="hidden_header"
    >
      <template v-slot:cell(Title)="data">
        <router-link :to="{ name: 'ProjectPageApply', params:{id:data.item.id}}" class="link">{{ data.item.project_title }}</router-link>
      </template>
      <template v-slot:cell(Admin)="data" v-if="isAdmin()">
        <button @click="gotoEditPage(data.item.id)" class="btn btn-link">Edit</button>
        /
        <button class="btn btn-link" @click="delBtn(data.item.id)">Delete</button>
      </template>
      <template v-slot:table-colgroup="scope">
        <col
          v-for="field in scope.fields"
          :key="field.key"
          :style="{ width: field.key === 'Admin' ? '200px' : ''}"
        />
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
export default {
  props: ["fields", "items"],
  data() {
    return {
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
      const msg = "Are your sure to delete the projects?";
      if (confirm(msg) == true) {
        deleteProject(id)
          .then((resp) => {
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
    isAdmin() {
      if (this.user == 3) {
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
};
</script>