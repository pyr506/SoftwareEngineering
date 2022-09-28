<template>
  <div>
    <ViewTitle></ViewTitle>
    <div class="contentBox">
      <p>You are welcome to join the platform and by joining and using the platform you are restricted by the following rules. The moderator of this platform (currently CCU as of February 2021) has the full right to ban any user who does not follow one or more of the following rules, without prior notification.</p>
      <br>
      <p>Rules to follow for using this platform:</p>
      <ol>
        <li>Conventional network ethics and etiquette are to be obeyed by all users of the platform including, but not limited to, ethical behavior and communications, use of only legal information and legal documents, etc.</li>
        <li>All information shared on this platform are the properties of their respective owners. The platform does not claim any rights on the shared information and documents and thus the platform is not liable for any kind of loss in any terms due to the direct or indirect use of re-sharing of the documents from this platform. All third party links and information are not the responsible of the platform, risks associated with third party links and websites must be totally borne by the users whoever clicks on the links or uses the third party websites.</li>
        <li>The owners of the platform (currently CCU as of 2021 February) have the full right to discontinue all services whenever it is not able to provide further services. All data shared here should be backed up by the users themselves, no backing up service is supported on this platform.</li>
        <li>Accidental deletion of information shared on this platform cannot be recovered, unless backed up by the users themselves, thus the platform is not liable to compensate for any loss due to accidental deletion.</li>
        <li>The services provided by this platform is purely voluntarily by the current owner of the platform (currently CCU as of February 2021), thus no fees will be charged to the users and no compensation of any sort will be provided for any kind of loss or otherwise.</li>
      </ol>
    </div>
    <div class="text-center">
      <b-form-checkbox
        id="checkbox"
        v-model="status"
        name="checkbox"
        value="accepted"
        unchecked-value="not_accepted"
      >I accept the terms and use</b-form-checkbox>
      <br />
      <b-button
        type="submit"
        variant="primary"
        :to="{ name: 'Register'}"
        :disabled="status === 'not_accepted'"
      >submit</b-button>
    </div>
  </div>
</template>
<script>
import ViewTitle from "../components/ViewTitle.vue";

export default {
  components: { ViewTitle },
  data() {
    return { status: "not_accepted" };
  },
  methods: {}
};
</script>
<style  scoped>
li {
  text-align: justify;
}
</style>