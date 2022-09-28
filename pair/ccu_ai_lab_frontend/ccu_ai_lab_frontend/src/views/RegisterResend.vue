<template>
  <div>
    <ViewTitle></ViewTitle>
    <div class="contentBox">
      1. Fill in your E-mail.<br>
      2. Click Resend button.<br>
      3. Confirmed mail will be sent to your e-mail, please check your mailbox.<br>
      4. Click the confirmed link to activate your account, thank you.<br>
      *Note: Please check your <font style="color: red">SPAM mailbox</font> if you did not receive Confirmed mail.
      <br>
      <br>
      <b-form v-if="show">
        <b-form-group id="input-group-1" label="Email address:" label-for="input-1">
          <b-form-input id="input-1" v-model="form.email" type="email" required></b-form-input>
        </b-form-group>
        <div class="text-center">
          <button class="btn btn-primary text-white" @click="onResend()" variant="primary" :disabled="isDisabled">Resend</button>
        </div>
      </b-form>
    </div>
  </div>
</template>

<script>
import { resend } from "../service/api.js";

import ViewTitle from "../components/ViewTitle.vue";

export default {
  components: { ViewTitle },
  data() {
    return {
      form: {
        email: ""
      },

      isDisabled: false,
      show: true
    };
  },
  methods: {
    onResend() {
      this.isDisabled= true;
      resend(this.form.email)
        .then((resp) => {
          if (resp.status == "error") {
            alert(resp.message);
          } else {
            alert("Resend Success: Confirmed mail has been resent to your e-mail, please check your mailbox, thank you.");
          }
        })
        .catch((error) => {
          alert("Resend Error: " + error.message);
          this.isDisabled=false;
        })
        .finally(() => {
          this.isDisabled=false;});
    }
  }
};
</script>