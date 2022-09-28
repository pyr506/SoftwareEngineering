<template>
  <div>
    <ViewTitle></ViewTitle>
    <div class="accordion" role="tablist">
      <b-card no-body class="mb-1">
        <b-card-header header-tag="header" class="p-1" role="tab">
          <b-button block v-b-toggle.accordion-1 variant="info">1. Connect your 'Projects of My Interest'.</b-button>
        </b-card-header>
        <b-collapse id="accordion-1" visible accordion="my-accordion" role="tabpanel">
          <b-card-body>
            <b-card-text>
              This system will automatically connect projects with your Areas of Interest.<br>
              1. Add your 'Projects of My Interest':<br>
              - Go to 'My Account/Profile/Projects of My Interest'.<br>
              - Choose the existing Interest.<br>
              <img src="../assets/img/Help/1_choose_fields.jpg"><br>
              - Or Add new Interest:<br>
              -- 1. Keyin new tag. <br>
              <img src="../assets/img/Help/1_add_fields_1.jpg"><br>
              <br>
              -- 2. Press Enter. <br>
              <img src="../assets/img/Help/1_add_fields_2.jpg"><br>
              -- 3. Click Save Button.<br>
              <br>
              2. Overview related 'Projects of My Interest':<br>
              - Go to 'Projects/Projects of My Interest'.
            </b-card-text>
          </b-card-body>
        </b-collapse>
      </b-card>

      <b-card no-body class="mb-1">
        <b-card-header header-tag="header" class="p-1" role="tab">
          <b-button block v-b-toggle.accordion-2 variant="info">2. Look for CO-PI of your project.</b-button>
        </b-card-header>
        <b-collapse id="accordion-2" accordion="my-accordion" role="tabpanel">
          <b-card-body>
            <b-card-text>
              In order to look for CO-PI, you have to add new project first.<br>
              1. Add new project and 'Projects of My Interest':<br>
              - Go to 'New Project'. <br>
              - Fill in all inputs of this form.<br>
              -- Note: If the current date exceeds 'Apply CO-PI End Date', everyone will not be able to apply.<br>
              - Add 'Projects of My Interest':<br>
              -- Choose the existing Interest.<br>
              <img src="../assets/img/Help/1_choose_fields.jpg"><br>
              -- Or Add new Interest:<br>
              --- 1. Keyin new tag. <br>
              <img src="../assets/img/Help/1_add_fields_1.jpg"><br>
              <br>
              --- 2. Press Enter. <br>
              <img src="../assets/img/Help/1_add_fields_2.jpg"><br>
              - Click Submit Button.<br>
              <br>
              2. Go to 'Projects/My Projects', you can see your all projects.<br>
              <br>
              3. You will receive a 'notification email' if someone applies for CO-PI of your project.<br>
              <br>
              4. Accept your CO-PI of your project:
              - Click title of a project to see detail of project.<br>
              - 'Apply CO-PI List' will have message if someone apples for CO-PI of your project.
              <img src="../assets/img/Help/2_ApplyCOPIList.jpg"><br>
              - Choose your CO-PIs from 'Apply CO-PI List'.<br>
              - Click Accept Button, the system will send a 'notification email' to the users you selected.

            </b-card-text>
          </b-card-body>
        </b-collapse>
      </b-card>

      <b-card no-body class="mb-1">
        <b-card-header header-tag="header" class="p-1" role="tab">
          <b-button block v-b-toggle.accordion-3 variant="info">3. Apply a project to be the CO-PI </b-button>
        </b-card-header>
        <b-collapse id="accordion-3" accordion="my-accordion" role="tabpanel">
          <b-card-body>
            <b-card-text>
              1. Click title of a project to see detail of project.<br>
              <br>
              2. Click 'Apply this project to be the CO-PI button', and fill in the reason why you want to be this project's CO-PI.<br>
              <img src="../assets/img/Help/3_ApplyCOPI.jpg"><br>
              <br>
              3. Click 'Apply Submit Button', the system will send a 'notification email' to the user of this project.<br>
              <br>
              4. 'Apply CO-PI List' will have your applied message.<br>
              <img src="../assets/img/Help/3_ApplyCOPIList.jpg"><br>
            </b-card-text>
          </b-card-body>
        </b-collapse>
      </b-card>

      <b-card no-body class="mb-1" v-if="isAdmin()">
        <b-card-header header-tag="header" class="p-1" role="tab">
          <b-button block v-b-toggle.accordion-4 variant="info">Admin 1. Block User </b-button>
        </b-card-header>
        <b-collapse id="accordion-4" accordion="my-accordion" role="tabpanel">
          <b-card-body>
            <b-card-text>
              Unconfirmed and Blocked User can not login.<br>
              1. Go to 'My Account/Users/Edit'.<br>
              <br>
              2. Select Confirmed (true: confirmed / false: Unconfirmed).<br>
              <br>
              3. Select Blockeded (true: Blocked / false: Unblocked).<br>
            </b-card-text>
          </b-card-body>
        </b-collapse>
      </b-card>
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
    },
  },
  created() {
  }
};
</script>
<style  scoped>
b-card-text img {
  border: #333 1px solid;
  width:80%;
}

</style>
