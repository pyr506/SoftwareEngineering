<template>
  <div>
    <ViewTitle></ViewTitle>
    <UserList :fields="fieldsAdmin" :items="items"></UserList>
  </div>
</template>

<script>
import { getUsers } from "../service/api.js";

import UserList from "../components/UserList.vue";
import ViewTitle from "../components/ViewTitle.vue";

export default {
  components: { UserList, ViewTitle },
  data() {
    return {
      fields: [],
      fieldsAdmin: [
        { key: "Username", label: "Username"},
        { key: "E-mail", label: "E-mail"},
        { key: "Country", label: "Country"},
        { key: "Company", label: "Company"},
        { key: "Job Title", label: "Job Title"},
        { key: "Confirmed", label: "Confirmed"},
        { key: "Blocked", label: "Blocked"},
        { key: "Admin", label: "Admin"}
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
        this.$router.push("/my_account/");
      }
    }
  },
  created() {
    getUsers().then(response => {
      const data = response.data;
      var result = data
      for (var i = result.length-1; i>=0 ; i--)
      {
        this.items.push({ user_id: data[i]['id'], username: data[i]['username'], email: data[i]['email'], country: data[i]['country'], company: data[i]['company'], job_title: data[i]['job_title'], confirmed: data[i]['confirmed'], blocked: data[i]['blocked']});
      }
    });
    this.isAdmin();
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
