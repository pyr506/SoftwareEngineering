<template>
  <div>
    <ViewTitle></ViewTitle>
    <div class="contentBox">
      <b-form>
        <div class="text-center" style="padding-bottom: 20px">
          Applier Infomation
        </div>
        <div class="row">
          <div class="col">
            <b-form-group
              id="input-group-2"
              label="Name of PI:"
              label-for="input-2"
            >
              <b-form-input
                id="input-2"
                v-model="name_of_pi"
                type="text"
                required
              ></b-form-input>
            </b-form-group>
          </div>
          <div class="col">
            <b-form-group
              id="input-group-3"
              label="Country:"
              label-for="input-3"
            >
              <b-form-select
                id="input-3"
                v-model="country"
                :options="countries"
                required
              ></b-form-select>
            </b-form-group>
          </div>
        </div>
        <div class="row">
          <div class="col">
            <b-form-group
              id="input-group-2"
              label="University:"
              label-for="input-2"
            >
              <b-form-input
                id="input-2"
                v-model="university"
                type="text"
                required
              ></b-form-input>
            </b-form-group>
          </div>
          <div class="col">
            <b-form-group
              id="input-group-3"
              label="Department:"
              label-for="input-3"
            >
              <b-form-input
                id="input-3"
                v-model="department"
                type="text"
                required
              ></b-form-input>
            </b-form-group>
          </div>
        </div>
        <div class="text-center" style="padding: 20px">Project Infomation</div>
        <b-form-group
          id="input-group-1"
          label="Title of your project:"
          label-for="input-1"
        >
          <b-form-input
            id="input-1"
            v-model="project_title"
            type="text"
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group id="input-group-1" label="Links:" label-for="input-1">
          <b-form-input
            id="input-1"
            v-model="link"
            type="url"
            required
          ></b-form-input>
        </b-form-group>
        <div class="row">
          <div class="col">
            <b-form-group
              id="input-group-1"
              label="Start Date:"
              label-for="startdate"
            >
              <b-form-datepicker
                id="startdate"
                v-model="start_date"
                class="mb-2"
              ></b-form-datepicker>
            </b-form-group>
          </div>
          <div class="col">
            <b-form-group
              id="input-group-1"
              label="End Date:"
              label-for="enddate"
            >
              <b-form-datepicker
                id="enddate"
                v-model="end_date"
                class="mb-2"
              ></b-form-datepicker>
            </b-form-group>
          </div>
        </div>
        <div class="row">
          <div class="col">
            <b-form-group
              id="input-group-4"
              label="Content:"
              label-for="textarea"
            >
              <TinymceEditor ref="editor" v-model="project_content">
              </TinymceEditor>
            </b-form-group>
          </div>
        </div>
        <b-form-group label="Research Area:" label-for="expertiseObj">
          <multiselect
            v-model="researches"
            tag-placeholder="Add this as new tag"
            placeholder="Search or add a tag"
            label="name"
            track-by="id"
            :options="options"
            :multiple="true"
            :taggable="true"
            @tag="addTag"
          >
          </multiselect>
        </b-form-group>
        <b-form-group
          id="input-group-1"
          label="Apply CO-PI End Date:"
          label-for="applyCOPIenddate"
        >
          <b-form-datepicker
            id="applyCOPIenddate"
            v-model="apply_copi_end_date"
            class="mb-2"
          ></b-form-datepicker>
        </b-form-group>
      </b-form>
      <br />
      <div class="text-center">
        <a
          class="btn btn-primary text-white"
          @click="onSubmit()"
          variant="primary"
          >Save</a
        >
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import {
  getSelfProject,
  getCOPIProjects,
  editProject,
  getAllResearch,
} from "../../service/api.js";
import Multiselect from "vue-multiselect";
import ViewTitle from "../../components/ViewTitle.vue";
import TinymceEditor from "../../components/TinymceEditor.vue";
export default {
  components: { ViewTitle, Multiselect, TinymceEditor },
  data() {
    return {
      user: localStorage.getItem("role_id"),

      project_user_id: "",
      project_title: "",
      name_of_pi: "",
      country: "",
      university: "",
      department: "",
      link: "",
      start_date: "",
      end_date: "",
      apply_copi_end_date: "",
      project_content: "",
      researches: [],

      options: [],

      COPIs: [],

      countries: [
        { text: "Albania", value: "AL" },
        { text: "Åland Islands", value: "AX" },
        { text: "Algeria", value: "DZ" },
        { text: "American Samoa", value: "AS" },
        { text: "Andorra", value: "AD" },
        { text: "Angola", value: "AO" },
        { text: "Anguilla", value: "AI" },
        { text: "Antarctica", value: "AQ" },
        { text: "Antigua and Barbuda", value: "AG" },
        { text: "Argentina", value: "AR" },
        { text: "Armenia", value: "AM" },
        { text: "Aruba", value: "AW" },
        { text: "Australia", value: "AU" },
        { text: "Austria", value: "AT" },
        { text: "Azerbaijan", value: "AZ" },
        { text: "Bahamas (the)", value: "BS" },
        { text: "Bahrain", value: "BH" },
        { text: "Bangladesh", value: "BD" },
        { text: "Barbados", value: "BB" },
        { text: "Belarus", value: "BY" },
        { text: "Belgium", value: "BE" },
        { text: "Belize", value: "BZ" },
        { text: "Benin", value: "BJ" },
        { text: "Bermuda", value: "BM" },
        { text: "Bhutan", value: "BT" },
        { text: "Bolivia (Plurinational State of)", value: "BO" },
        { text: "Bonaire, Sint Eustatius and Saba", value: "BQ" },
        { text: "Bosnia and Herzegovina", value: "BA" },
        { text: "Botswana", value: "BW" },
        { text: "Bouvet Island", value: "BV" },
        { text: "Brazil", value: "BR" },
        { text: "British Indian Ocean Territory (the)", value: "IO" },
        { text: "Brunei Darussalam", value: "BN" },
        { text: "Bulgaria", value: "BG" },
        { text: "Burkina Faso", value: "BF" },
        { text: "Burundi", value: "BI" },
        { text: "Cabo Verde", value: "CV" },
        { text: "Cambodia", value: "KH" },
        { text: "Cameroon", value: "CM" },
        { text: "Canada", value: "CA" },
        { text: "Cayman Islands (the)", value: "KY" },
        { text: "Central African Republic (the)", value: "CF" },
        { text: "Chad", value: "TD" },
        { text: "Chile", value: "CL" },
        { text: "China", value: "CN" },
        { text: "Christmas Island", value: "CX" },
        { text: "Cocos (Keeling) Islands (the)", value: "CC" },
        { text: "Colombia", value: "CO" },
        { text: "Comoros (the)", value: "KM" },
        { text: "Congo (the Democratic Republic of the)", value: "CD" },
        { text: "Congo (the)", value: "CG" },
        { text: "Cook Islands (the)", value: "CK" },
        { text: "Costa Rica", value: "CR" },
        { text: "Croatia", value: "HR" },
        { text: "Cuba", value: "CU" },
        { text: "Curaçao", value: "CW" },
        { text: "Cyprus", value: "CY" },
        { text: "Czechia", value: "CZ" },
        { text: "Côte d'Ivoire", value: "CI" },
        { text: "Denmark", value: "DK" },
        { text: "Djibouti", value: "DJ" },
        { text: "Dominica", value: "DM" },
        { text: "Dominican Republic (the)", value: "DO" },
        { text: "Ecuador", value: "EC" },
        { text: "Egypt", value: "EG" },
        { text: "El Salvador", value: "SV" },
        { text: "Equatorial Guinea", value: "GQ" },
        { text: "Eritrea", value: "ER" },
        { text: "Estonia", value: "EE" },
        { text: "Eswatini", value: "SZ" },
        { text: "Ethiopia", value: "ET" },
        { text: "Falkland Islands (the) [Malvinas]", value: "FK" },
        { text: "Faroe Islands (the)", value: "FO" },
        { text: "Fiji", value: "FJ" },
        { text: "Finland", value: "FI" },
        { text: "France", value: "FR" },
        { text: "French Guiana", value: "GF" },
        { text: "French Polynesia", value: "PF" },
        { text: "French Southern Territories (the)", value: "TF" },
        { text: "Gabon", value: "GA" },
        { text: "Gambia (the)", value: "GM" },
        { text: "Georgia", value: "GE" },
        { text: "Germany", value: "DE" },
        { text: "Ghana", value: "GH" },
        { text: "Gibraltar", value: "GI" },
        { text: "Greece", value: "GR" },
        { text: "Greenland", value: "GL" },
        { text: "Grenada", value: "GD" },
        { text: "Guadeloupe", value: "GP" },
        { text: "Guam", value: "GU" },
        { text: "Guatemala", value: "GT" },
        { text: "Guernsey", value: "GG" },
        { text: "Guinea", value: "GN" },
        { text: "Guinea-Bissau", value: "GW" },
        { text: "Guyana", value: "GY" },
        { text: "Haiti", value: "HT" },
        { text: "Heard Island and McDonald Islands", value: "HM" },
        { text: "Holy See (the)", value: "VA" },
        { text: "Honduras", value: "HN" },
        { text: "Hong Kong", value: "HK" },
        { text: "Hungary", value: "HU" },
        { text: "Iceland", value: "IS" },
        { text: "India", value: "IN" },
        { text: "Indonesia", value: "ID" },
        { text: "Iran (Islamic Republic of)", value: "IR" },
        { text: "Iraq", value: "IQ" },
        { text: "Ireland", value: "IE" },
        { text: "Isle of Man", value: "IM" },
        { text: "Israel", value: "IL" },
        { text: "Italy", value: "IT" },
        { text: "Jamaica", value: "JM" },
        { text: "Japan", value: "JP" },
        { text: "Jersey", value: "JE" },
        { text: "Jordan", value: "JO" },
        { text: "Kazakhstan", value: "KZ" },
        { text: "Kenya", value: "KE" },
        { text: "Kiribati", value: "KI" },
        { text: "Korea (the Democratic People's Republic of)", value: "KP" },
        { text: "Korea (the Republic of)", value: "KR" },
        { text: "Kuwait", value: "KW" },
        { text: "Kyrgyzstan", value: "KG" },
        { text: "Lao People's Democratic Republic (the)", value: "LA" },
        { text: "Latvia", value: "LV" },
        { text: "Lebanon", value: "LB" },
        { text: "Lesotho", value: "LS" },
        { text: "Liberia", value: "LR" },
        { text: "Libya", value: "LY" },
        { text: "Liechtenstein", value: "LI" },
        { text: "Lithuania", value: "LT" },
        { text: "Luxembourg", value: "LU" },
        { text: "Macao", value: "MO" },
        { text: "Madagascar", value: "MG" },
        { text: "Malawi", value: "MW" },
        { text: "Malaysia", value: "MY" },
        { text: "Maldives", value: "MV" },
        { text: "Mali", value: "ML" },
        { text: "Malta", value: "MT" },
        { text: "Marshall Islands (the)", value: "MH" },
        { text: "Martinique", value: "MQ" },
        { text: "Mauritania", value: "MR" },
        { text: "Mauritius", value: "MU" },
        { text: "Mayotte", value: "YT" },
        { text: "Mexico", value: "MX" },
        { text: "Micronesia (Federated States of)", value: "FM" },
        { text: "Moldova (the Republic of)", value: "MD" },
        { text: "Monaco", value: "MC" },
        { text: "Mongolia", value: "MN" },
        { text: "Montenegro", value: "ME" },
        { text: "Montserrat", value: "MS" },
        { text: "Morocco", value: "MA" },
        { text: "Mozambique", value: "MZ" },
        { text: "Myanmar", value: "MM" },
        { text: "Namibia", value: "NA" },
        { text: "Nauru", value: "NR" },
        { text: "Nepal", value: "NP" },
        { text: "Netherlands (the)", value: "NL" },
        { text: "New Caledonia", value: "NC" },
        { text: "New Zealand", value: "NZ" },
        { text: "Nicaragua", value: "NI" },
        { text: "Niger (the)", value: "NE" },
        { text: "Nigeria", value: "NG" },
        { text: "Niue", value: "NU" },
        { text: "Norfolk Island", value: "NF" },
        { text: "Northern Mariana Islands (the)", value: "MP" },
        { text: "Norway", value: "NO" },
        { text: "Oman", value: "OM" },
        { text: "Pakistan", value: "PK" },
        { text: "Palau", value: "PW" },
        { text: "Palestine, State of", value: "PS" },
        { text: "Panama", value: "PA" },
        { text: "Papua New Guinea", value: "PG" },
        { text: "Paraguay", value: "PY" },
        { text: "Peru", value: "PE" },
        { text: "Philippines (the)", value: "PH" },
        { text: "Pitcairn", value: "PN" },
        { text: "Poland", value: "PL" },
        { text: "Portugal", value: "PT" },
        { text: "Puerto Rico", value: "PR" },
        { text: "Qatar", value: "QA" },
        { text: "Republic of North Macedonia", value: "MK" },
        { text: "Romania", value: "RO" },
        { text: "Russian Federation (the)", value: "RU" },
        { text: "Rwanda", value: "RW" },
        { text: "Réunion", value: "RE" },
        { text: "Saint Barthélemy", value: "BL" },
        { text: "Saint Helena, Ascension and Tristan da Cunha", value: "SH" },
        { text: "Saint Kitts and Nevis", value: "KN" },
        { text: "Saint Lucia", value: "LC" },
        { text: "Saint Martin (French part)", value: "MF" },
        { text: "Saint Pierre and Miquelon", value: "PM" },
        { text: "Saint Vincent and the Grenadines", value: "VC" },
        { text: "Samoa", value: "WS" },
        { text: "San Marino", value: "SM" },
        { text: "Sao Tome and Principe", value: "ST" },
        { text: "Saudi Arabia", value: "SA" },
        { text: "Senegal", value: "SN" },
        { text: "Serbia", value: "RS" },
        { text: "Seychelles", value: "SC" },
        { text: "Sierra Leone", value: "SL" },
        { text: "Singapore", value: "SG" },
        { text: "Sint Maarten (Dutch part)", value: "SX" },
        { text: "Slovakia", value: "SK" },
        { text: "Slovenia", value: "SI" },
        { text: "Solomon Islands", value: "SB" },
        { text: "Somalia", value: "SO" },
        { text: "South Africa", value: "ZA" },
        { text: "South Georgia and the South Sandwich Islands", value: "GS" },
        { text: "South Sudan", value: "SS" },
        { text: "Spain", value: "ES" },
        { text: "Sri Lanka", value: "LK" },
        { text: "Sudan (the)", value: "SD" },
        { text: "Suriname", value: "SR" },
        { text: "Svalbard and Jan Mayen", value: "SJ" },
        { text: "Sweden", value: "SE" },
        { text: "Switzerland", value: "CH" },
        { text: "Syrian Arab Republic", value: "SY" },
        { text: "Taiwan (Republic of China)", value: "TW" },
        { text: "Tajikistan", value: "TJ" },
        { text: "Tanzania, United Republic of", value: "TZ" },
        { text: "Thailand", value: "TH" },
        { text: "Timor-Leste", value: "TL" },
        { text: "Togo", value: "TG" },
        { text: "Tokelau", value: "TK" },
        { text: "Tonga", value: "TO" },
        { text: "Trinidad and Tobago", value: "TT" },
        { text: "Tunisia", value: "TN" },
        { text: "Turkey", value: "TR" },
        { text: "Turkmenistan", value: "TM" },
        { text: "Turks and Caicos Islands (the)", value: "TC" },
        { text: "Tuvalu", value: "TV" },
        { text: "Uganda", value: "UG" },
        { text: "Ukraine", value: "UA" },
        { text: "United Arab Emirates (the)", value: "AE" },
        {
          text: "United Kingdom of Great Britain and Northern Ireland (the)",
          value: "GB",
        },
        { text: "United States Minor Outlying Islands (the)", value: "UM" },
        { text: "United States of America (the)", value: "US" },
        { text: "Uruguay", value: "UY" },
        { text: "Uzbekistan", value: "UZ" },
        { text: "Vanuatu", value: "VU" },
        { text: "Venezuela (Bolivarian Republic of)", value: "VE" },
        { text: "Viet Nam", value: "VN" },
        { text: "Virgin Islands (British)", value: "VG" },
        { text: "Virgin Islands (U.S.)", value: "VI" },
        { text: "Wallis and Futuna", value: "WF" },
        { text: "Western Sahara", value: "EH" },
        { text: "Yemen", value: "YE" },
        { text: "Zambia", value: "ZM" },
        { text: "Zimbabwe", value: "ZW" },
      ],
    };
  },
  methods: {
    onSubmit() {
      editProject(
        window.location.hash.split("/")[3],
        this.researches,
        this.country,
        this.university,
        this.name_of_pi,
        this.department,
        this.project_title,
        this.link,
        this.start_date,
        this.end_date,
        this.apply_copi_end_date,
        this.project_content
      )
        .then((response) => {
          if (response.status == "error") {
            throw new Error(response.message);
          }
          alert("Edit Project Success");
          const backURL = "/" + window.location.hash.split("/")[1];
          this.$router.push(backURL);
        })
        .catch((error) => {
          alert("Edit Project Error: " + error.message);
          console.log(error);
        });
    },
    addTag(newTag) {
      const tag = {
        name: newTag,
        id: newTag.substring(0, 2) + Math.floor(Math.random() * 10000000),
      };
      this.options.push(tag);
      this.researches.push(tag);
    },
    isAdmin() {
      if (this.user == 3) {
        return true;
      } else {
        return false;
      }
    },
    isUserID(compare_user_id) {
      if (localStorage.getItem("id") == compare_user_id) {
        return true;
      } else {
        return false;
      }
    },
  },
  created() {
    getSelfProject(window.location.hash.split("/")[3]).then((response) => {
      this.project_user_id = response.data.user_id;
      this.project_title = response.data.project_title;
      this.name_of_pi = response.data.name_of_pi;
      this.country = response.data.country;
      this.university = response.data.university;
      this.department = response.data.department;
      this.link = response.data.link;
      this.start_date = response.data.start_date;
      this.end_date = response.data.end_date;
      this.apply_copi_end_date = response.data.apply_copi_end_date;
      this.project_content = response.data.project_content;
      this.researches = response.data.researches;

      getCOPIProjects(window.location.hash.split("/")[3]).then((response) => {
        const data = response.data;
        const result = data;
        this.COPIs.push(result);
      });

      if (this.isAdmin() || this.isUserID(this.project_user_id)) {
        //Admin or Owner => see all
        return true;
      } //not Owner => go out
      else {
        this.$router.push("/projects/" + window.location.hash.split("/")[3]);
      }
    }),
      getAllResearch().then((response) => {
        const exp_data = response.data;
        var i = 0;
        for (i = 0; i < exp_data.length; i++) {
          this.options.push(exp_data[i]);
        }
      });
  },
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
