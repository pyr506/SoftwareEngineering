<template>
  <div>
    <ViewTitle></ViewTitle>
    <div class="contentBox">
      <b-form @submit="onSubmit" @reset="onReset" v-if="show">
        <b-form-group id="input-group-2" label="Title:" label-for="input-2">
          <b-form-input id="input-2" v-model="form.name" required></b-form-input>
        </b-form-group>

        <b-form-group id="input-group-3" label="Question Type:" label-for="input-3">
          <b-form-select id="input-3" v-model="form.type" :options="questionTypes" required></b-form-select>
        </b-form-group>
        <b-form-group id="input-group-4" label="Content:" label-for="textarea">
          <b-form-textarea id="textarea" v-model="text" rows="5"></b-form-textarea>
        </b-form-group>

        <div class="text-center">
          <b-button type="submit" variant="primary">Submit</b-button>
        </div>
      </b-form>
    </div>
  </div>
</template>

<script>
import ViewTitle from "../components/ViewTitle.vue";

export default {
  components: {
    ViewTitle
  },
  data() {
    return {
      form: {
        email: "",
        name: "",
        type: null,
        checked: []
      },
      questionTypes: [
        { text: "Select One", value: null },
        "問題一",
        "問題二",
        "問題三",
        "問題四",
        "其他"
      ],
      show: true,
      text: ""
    };
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      alert(JSON.stringify(this.form));
    },
    onReset(evt) {
      evt.preventDefault();
      // Reset our form values
      this.form.email = "";
      this.form.name = "";
      this.form.type = null;
      this.form.checked = [];
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    }
  }
};
</script>