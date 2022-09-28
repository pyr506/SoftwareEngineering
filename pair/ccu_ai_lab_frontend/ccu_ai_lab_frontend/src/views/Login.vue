<template>
  <div>
    <ViewTitle></ViewTitle>
    <div class="contentBox">
      <b-form v-if="show">
        <b-form-group id="input-group-1" label="Email address:" label-for="input-1">
          <b-form-input id="input-1" v-model="form.email" type="email" required></b-form-input>
        </b-form-group>

        <b-form-group id="input-group-2" label="Password:" label-for="input-2">
          <b-form-input id="input-2" v-model="form.password" type="password" required></b-form-input>
        </b-form-group>
        <div class="text-center">
          <a class="btn btn-primary text-white" @click="onSubmit()" variant="primary">Login</a>
        </div>
        <div class="text-center">
          <br>
          <router-link style="color: red" :to="{ name: 'Forget Password'}" class="link">Forget Password</router-link>
          <br>
          <router-link style="color: red" :to="{ name: 'RegisterResend'}" class="link">Resend Confirmed Mail</router-link>
        </div>
      </b-form>
    </div>
  </div>
</template>

<script>
import { login } from "../service/api.js";

import ViewTitle from "../components/ViewTitle.vue";

export default {
  components: { ViewTitle },
  data() {
    return {
      form: {
        email: "",
        password: ""
      },

      show: true
    };
  },
  methods: {
    onSubmit() {
      login(this.form.email, this.form.password)
        .then(resp => {
          if (resp.status == "error") {
            alert(resp.message);
          } else {
            this.$store.state.isLogin = true;
            localStorage.setItem("token", resp.data.access_token);
            localStorage.setItem("id", resp.data.user.id);
            localStorage.setItem("username", resp.data.user.username);
            if (resp.data.user.role == "Administrator") {
              localStorage.setItem("role_id", 3);
            } else if (resp.data.user.role == "Moderator") {
              localStorage.setItem("role_id", 2);
            } else if (resp.data.user.role == "User") {
              localStorage.setItem("role_id", 1);
            }
            alert("Login Success");
            this.$router.push("/projects");
          }
        })
        .catch(error => {
          alert(error.message);
        });
    }
  }
};
</script>
