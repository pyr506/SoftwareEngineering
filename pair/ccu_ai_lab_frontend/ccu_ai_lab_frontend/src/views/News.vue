<template>
  <div>
    <ViewTitle></ViewTitle>
    <NewsList :fields="fields" :items="items"></NewsList>
  </div>
</template>

<script>
import axios from "axios";
import { getNews } from "../service/api.js";

import NewsList from "../components/NewsList.vue";
import ViewTitle from "../components/ViewTitle.vue";

export default {
  components: { NewsList, ViewTitle },
  data() {
    return {
      fields: [],
      fieldsAdmin: [
        { key: "Title", label: "Title"},
        { key: "Clicked", label: "Clicked"},
        { key: "DateTime(GMT)", label: "DateTime(GMT)"},
        { key: "Admin", label: "Admin"}
      ],
      
      fieldsUser: [
        { key: "Title", label: "Title"},
        { key: "Clicked", label: "Clicked"},
        { key: "DateTime(GMT)", label: "DateTime(GMT)"}
      ],
      items: [],
      user: localStorage.getItem("role_id")
    };
  },
  computed: {
    rows() {
      return this.items.length;
    },
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
    getNews().then(response => {
      const data = response.data;
      var result = data
      for (var i = result.length-1; i>=0 ; i--)
      {
        this.items.push({ news_id: data[i]['id'], news_title: data[i]['title'], clicked: data[i]['clicked'], created_at: data[i]['created_at']} );
      }
    });
    this.getFields();
  }
};
</script>

<style>

.table-condensed {
  font-size: 10px;
}

table[aria-colindex="2"] {
  opacity: 0.5;
  font-size: 5px;
}
</style>
