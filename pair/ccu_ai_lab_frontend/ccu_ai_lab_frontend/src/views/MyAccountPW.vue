<template>
  <div>
    <ViewTitle></ViewTitle>
    <div class="contentBox">
      <b-form @submit.prevent="onSubmit">
        <b-form-group id="input-group-1" label="Current password:" label-for="input-1">
          <b-form-input id="input-1" v-model="form.password" type="password" required></b-form-input>
        </b-form-group>
        <b-form-group id="input-group-2" label="New password:" label-for="input-2">
          <b-form-input id="input-2" v-model="form.new_password" type="password" required></b-form-input>
        </b-form-group>
        <b-form-group id="input-group-3" label="Confirm new password:" label-for="input-3">
          <b-form-input id="input-3" v-model="form.confirm_password" type="password" required></b-form-input>
        </b-form-group>
        <div class="text-center">
          <b-button type="submit" variant="primary">Submit</b-button>
        </div>
      </b-form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { changePW } from "../service/api.js";
import ViewTitle from "../components/ViewTitle.vue";

export default {
  components: { ViewTitle },
  data() {
    return {
      form: {
        new_password: "",
        password: "",
        confirm_password: ""
      }
    };
  },
  methods: {
    onSubmit() {
      changePW(
        this.form.password,
        this.form.new_password,
        this.form.confirm_password
      )
        .then(resp => {
          alert("Your password has been changed.");
          localStorage.removeItem("token");
          localStorage.removeItem("id");
          localStorage.removeItem("username");
          localStorage.removeItem("role_id");
          this.$store.state.isLogin = false;
          this.$router.push("/").catch(() => {});
        })
        .catch(error => {
          alert(error.message);
          this.form.password = "";
          this.form.new_password = "";
          this.form.confirm_password = "";
        });
    }
  }
};
</script>
