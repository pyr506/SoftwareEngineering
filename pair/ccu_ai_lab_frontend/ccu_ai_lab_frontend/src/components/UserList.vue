<template>
  <div>
    <template>
      <div>
        <b-table
          :fields="fields"
          :items="items"
          :per-page=20
          :current-page="currentPage"
        >
          <template v-slot:cell(Username)="data">
            <router-link :to="{ name: 'UserPage', params:{id:data.item.user_id}}" class="link">{{ data.item.username }}</router-link>
          </template>
          <template v-slot:cell(E-mail)="data">{{ data.item.email }}</template>
          <template v-slot:cell(Country)="data">{{ data.item.country }}</template>
          <template v-slot:cell(Company)="data">{{ data.item.company }}</template>
          <template v-slot:cell(Job Title)="data">{{ data.item.job_title }}</template>
          <template v-slot:cell(Confirmed)="data">{{ data.item.confirmed }}</template>
          <template v-slot:cell(Blocked)="data">{{ data.item.blocked }}</template>
          <template v-slot:cell(Admin)="data" v-if="isAdmin()" >
            <button  @click="gotoEditPage(data.item.user_id)" class="btn btn-link">Edit</button>
          </template>
          <template v-slot:table-colgroup="scope">
              <col
                v-for="field in scope.fields"
                :key="field.key"
              />
          </template>
        </b-table>
        <b-pagination
          v-model="currentPage"
          :total-rows="rows"
          :per-page=20
          aria-controls="my-table"
          align="right"
        ></b-pagination>
      </div>
    </template>
  </div>
</template>

<script>
import { blockuser } from "../service/api.js";

export default {
  components: {},
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
    gotoPage(id) {
      this.$router.push(`/users/` + id);
    },
    gotoEditPage(id) {
      this.$router.push(`/users/edit/` + id);
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
    blockBtn(id) {
      const msg = "Are your sure to block the user?";
      if (confirm(msg) == true) {
        blockuser(id)
          .then((response) => {
            if (response.status == 'error')
            {
              throw new Error(response.message);
            }
            alert("Block User Success");
            window.location.reload();
          })
          .catch((error) => {
            alert("Block User Error:" + error);
          });
      }
    }
  }
};
</script>