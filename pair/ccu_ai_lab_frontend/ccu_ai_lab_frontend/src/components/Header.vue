<template>
<div>
  <div class="header">
    <img src="../assets/img/TWIN_Banner.png">
    <div class="Loginfo">
      <div v-if="!isLogin()">
        <b-button type="submit" variant="light" :to="{ name: 'Login'}">Login</b-button>
      </div>
      <div v-else>
        <div id="username">{{ username }}, hello</div>
        <b-button type="submit" variant="light" v-b-modal.modal-1>Logout</b-button>
      </div>
      <b-modal id="modal-1" title="Confirm Logout" @ok="handleOk">
        <p class="text-center">Are your sure to logout?</p>
      </b-modal>
    </div>
  </div>
</div>
</template>

<script>
import axios from "axios";
import { logout } from "../service/api.js";
export default {
  data() {
    return {
      username:"",
    };
  },
  methods: {
    handleOk() {
      logout()
        .then(resp => {
          this.$store.state.isLogin = false;
          localStorage.removeItem("token");
          localStorage.removeItem("id");
          localStorage.removeItem("username");
          localStorage.removeItem("role_id");
          alert("Logout Success");
          this.$router.push("/").catch(() => {});
        })
        .catch(error => {
          console.log(error.message);
          this.$store.state.isLogin = false;
          localStorage.removeItem("token");
          localStorage.removeItem("id");
          localStorage.removeItem("username");
          localStorage.removeItem("role_id");
          this.$router.push("/").catch(() => {});
        });
    },
    isLogin() {
      this.username = localStorage.getItem("username");
      return this.$store.state.isLogin;
    },
  },
  created() {
  }
};
</script>

<style scoped>
.header {
  position: relative;
  padding: 0px;
  max-width: 1400px;
  max-height: 400px;
  margin: 0 auto;
  text-align: center;
  
}
.header img{
  width: 100%;
  margin: 0 auto;
  text-align: center;
}
.Loginfo {
  position: absolute;
  text-align: right;
  top:20px;
  right:20px;
}
#username {
  color:white;
}

@media (max-width: 576px) {
  .Loginfo {
    top:1px;
    right:1px
  }
  #username {
    font-size: 0.8rem;
    float: left;
  }
  .Loginfo div button {
    font-size: 0.8rem;
    width:4rem;
    padding: 0px;
    margin:1px;
  }

}
</style>