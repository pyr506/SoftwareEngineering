<template>
  <div>
    <ViewTitle></ViewTitle>
    <div class="row text-center">
      <div class="col myAccountBox">
        <router-link :to="{ name: 'Change Password'}">
          <b-button variant="outline-secondary">
            <b-icon icon="lock" style="width: 150px; height: 150px; padding:10px"></b-icon>
            <br />Password
          </b-button>
        </router-link>
      </div>
      <div class="col myAccountBox">
        <router-link :to="{ name: 'Change Personal Information'}">
          <b-button variant="outline-secondary ">
            <b-icon icon="person" style="width: 150px; height: 150px;"></b-icon>
            <br />Profile
          </b-button>
        </router-link>
      </div>
    </div>
    <div class="row text-center" v-if="isAdmin()">
      <div class="col myAccountBox">
        <router-link :to="{ name: 'Edit Webinfos'}">
          <b-button variant="outline-secondary">
            <b-icon icon="info-circle-fill" style="width: 150px; height: 150px; padding:10px"></b-icon>
            <br />Web Information
          </b-button>
        </router-link>
      </div>
      <div class="col myAccountBox">
        <router-link :to="{ name: 'Users'}">
          <b-button variant="outline-secondary ">
            <b-icon icon="person-lines-fill" style="width: 150px; height: 150px;"></b-icon>
            <br />Users
          </b-button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import ViewTitle from "../components/ViewTitle.vue";

export default {
  components: { ViewTitle },
  data() {
    return {
      user: localStorage.getItem("role_id")
    };
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
    }
  },
};
</script>

<style>
.myAccountBox {
  padding: 20px;
  margin: 20px;
  min-height: 250px;
  color: grey;
  font-size: 20px;
}

.accont-link a:hover {
  color: #3ab795;
  text-decoration: none;
}

.accont-link a {
  color: rgb(63, 63, 63);
}
</style>
