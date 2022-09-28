<template>
  <div>
    <ViewTitle></ViewTitle>
    <div class="contentBox">
      Registration steps:<br />
      1. Fill in your E-mail, User Name, Password, Confirm Password.<br />
      2. Click Submit button.<br />
      3. Confirmed mail will be sent to your e-mail, please check your
      mailbox.<br />
      4. Click the confirmed link to activate your account, thank you.<br />
      *Note: Please check your <font style="color: red">SPAM mailbox</font> if
      you did not receive Confirmed mail or
      <router-link
        style="color: red"
        :to="{ name: 'RegisterResend' }"
        class="link"
        >Resend</router-link
      >.
      <br />
      <br />
      <b-form>
        <b-form-group id="input-group-3" label="E-mail:" label-for="input-1">
          <b-form-input
            id="input-1"
            v-model="form.email"
            type="email"
            required
          ></b-form-input>
        </b-form-group>

        <b-form-group id="input-group-3" label="User Name:" label-for="input-2">
          <b-form-input
            id="input-2"
            v-model="form.username"
            type="text"
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group id="input-group-5" label="Password:" label-for="input-3">
          <b-form-input
            id="input-3"
            v-model="form.password"
            type="password"
            required
          ></b-form-input>
        </b-form-group>

        <b-form-group
          id="input-group-5"
          label="Confirm Password:"
          label-for="input-4"
        >
          <b-form-input
            id="input-4"
            v-model="form.confirm_password"
            type="password"
            required
          ></b-form-input>
        </b-form-group>

        <div class="text-center">
          <button
            class="btn btn-primary text-white"
            @click="onSubmit()"
            variant="primary"
            :disabled="isDisabled"
          >
            Submit
          </button>
        </div>
      </b-form>
    </div>
  </div>
</template>

<script>
import { register } from "../service/api.js";

import ViewTitle from "../components/ViewTitle.vue";

export default {
  components: { ViewTitle },
  data() {
    return {
      form: {
        email: "",
        username: "",
        password: "",
        confirm_password: "",
      },
      isDisabled: false,
    };
  },
  methods: {
    onSubmit() {
      this.isDisabled = true;
      register(
        this.form.email,
        this.form.username,
        this.form.password,
        this.form.confirm_password
      )
        .then((resp) => {
          console.log(resp);
          if (resp.status == "error") {
            throw new Error(resp.message);
          }
          //localStorage.token = resp.data.access_token;
          alert(
            "Register Success: Confirmation mail has been sent to your e-mail, please check your mailbox, thank you."
          );
          this.$router.push("/");
        })
        .catch((error) => {
          console.log(error);
          alert("Register Error: " + error.message);
          this.form.email = "";
          this.form.username = "";
          this.form.password = "";
          this.form.confirm_password = "";
          this.isDisabled = false;
        })
        .finally(function () {
          this.isDisabled = false;
        });
    },
  },
};
</script>
