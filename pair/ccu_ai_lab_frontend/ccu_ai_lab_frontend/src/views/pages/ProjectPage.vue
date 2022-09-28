<template>
  <div>
    <h2>
      <strong>▹ {{ project_title }}</strong>
    </h2>
    <hr />
    <div class="contentBox">
      <div class="text-center" style="padding-bottom: 20px">
        Applier Infomation
      </div>
      <div class="row">
        <div class="col">
          <div class="contentBox">
            User Name:
            <router-link
              :to="{ name: 'UserPage', params: { id: project_user_id } }"
              class="link"
              >{{ project_user_name }}</router-link
            >
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <div class="contentBox">Name of PI: {{ name_of_pi }}</div>
        </div>
        <div class="col">
          <div class="row">
            <div class="col">
              <div class="contentBox">Country:</div>
            </div>
            <div class="col">
              <b-form-select
                style="width: 250px"
                id="input-3"
                v-model="country"
                :options="countries"
                disabled
              ></b-form-select>
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <div class="contentBox">University: {{ university }}</div>
        </div>
        <div class="col">
          <div class="contentBox">Department: {{ department }}</div>
        </div>
      </div>
    </div>
    <div class="text-center" style="padding: 20px">Project Infomation</div>
    <div class="contentBox">
      Link: <a :href="link" target="_blank">{{ link }}</a>
    </div>
    <div class="contentBox">
      Date: {{ dateFormat(start_date) }} - {{ dateFormat(end_date) }}
    </div>
    <div class="contentBox">
      Content:
      <TinymceViewer ref="editor" v-model="project_content"> </TinymceViewer>
    </div>
    <div class="contentBox">
      <b-form-group label="Research Area:" label-for="expertiseObj">
        <multiselect
          id="expertiseObj"
          v-model="researches"
          tag-placeholder="Add this as new tag"
          placeholder="Search or add a tag"
          label="name"
          track-by="id"
          :options="exp"
          :multiple="true"
          :taggable="true"
          disabled
        ></multiselect>
      </b-form-group>
    </div>
    <div class="contentBox" v-bind:style="{ color: activeColor }">
      Apply CO-PI End Date: {{ dateFormat(apply_copi_end_date) }}
    </div>
    <div class="contentBox">
      <b-form>
        Apply CO-PI List:
        <div class="table">
          <tr v-for="COPI in COPIs[0]" v-bind:key="COPI.id">
            <td>
              <input type="checkbox" v-model="COPI.accepted" />
            </td>
            <td>
              <label for="checkbox"
                ><router-link
                  :to="{ name: 'UserPage', params: { id: COPI.user_id } }"
                  class="link"
                  >{{ COPI.user_name }}</router-link
                >
              </label>
            </td>
            <td>{{ COPI.COPI_content }}</td>
            <td>{{ COPI.updated_at }} (GMT)</td>
          </tr>
        </div>
        <div class="contentBox" v-if="isShowAccept">
          Accept the project's CO-PI:
          <div class="text-center">
            <button
              id="btnAccept"
              class="btn btn-primary text-white"
              @click="btnAccept()"
              variant="primary"
              :disabled="isDisabled"
            >
              Accept
            </button>
          </div>
        </div>
      </b-form>
    </div>
    <div class="contentBox" v-if="isShowApply">
      <div class="applyBtn text-center">
        <b-button v-b-toggle.collapse-1 variant="outline-info" size="sm"
          >Apply this project to be the CO-PI.</b-button
        >
      </div>
      <b-collapse id="collapse-1" class="mt-2">
        <b-card>
          <div class="formBox">
            <b-form>
              <b-form-group
                id="input-group-4"
                label="Describe the reason why you want to be the project's CO-PI:"
                label-for="textarea"
              >
                <b-form-textarea
                  id="textarea"
                  v-model="form.COPI_project_content"
                  rows="10"
                ></b-form-textarea>
              </b-form-group>
              <div class="text-center">
                <button
                  class="btn btn-primary text-white"
                  @click="btnApply()"
                  variant="primary"
                  :disabled="isApplyDisabled"
                >
                  Apply Submit
                </button>
              </div>
            </b-form>
          </div>
        </b-card>
      </b-collapse>
    </div>
    <div class="text-right contentBox">
      <b-button pill variant="outline-secondary" @click="$router.go(-1)"
        >back</b-button
      >
    </div>
  </div>
</template>
<script>
import {
  getSelfProject,
  newCOPIProject,
  getAllResearch,
  getCOPIProjects,
  editCOPIAccepted,
} from "../../service/api.js";
import Multiselect from "vue-multiselect";
import TinymceViewer from "../../components/TinymceViewer.vue";
export default {
  prop: ["id"],
  props: {
    from: String,
  },
  components: {
    Multiselect,
    TinymceViewer,
  },
  data() {
    return {
      form: {
        project_id: "",
        COPI_project_content: "",
        Accpted: [],
      },
      user: localStorage.getItem("role_id"),
      isApplyDisabled: false,
      isDisabled: false,
      isShowApply: false,
      isShowAccept: false,
      success_count: 0,
      activeColor: "",

      project_user_id: "",
      project_user_name: "",
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
      isProjectUserID: false,

      exp: [{}],

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
  created() {
    getSelfProject(window.location.hash.split("/")[2]).then((response) => {
      this.project_user_id = response.data.user_id;
      this.project_user_name = response.data.user_name;
      this.project_title = response.data.project_title;
      this.name_of_pi = response.data.name_of_pi;
      this.country = response.data.country;
      this.university = response.data.university;
      this.department = response.data.department;
      this.link = response.data.link;
      this.start_date = this.dateFormat(response.data.start_date);
      this.end_date = this.dateFormat(response.data.end_date);
      this.apply_copi_end_date = this.dateFormat(
        response.data.apply_copi_end_date
      );
      this.project_content = response.data.project_content;
      this.researches = response.data.researches;

      getCOPIProjects(window.location.hash.split("/")[2]).then((response) => {
        const data = response.data;
        var result = data;

        //authorization control
        if (this.isAdmin()) {
          //Admin => see all, show apply btn if not apply
          this.COPIs.push(result);
          if (this.isUserID(this.project_user_id)) {
            this.isShowApply = false;
          } else {
            this.isShowApply = true;
          }
          for (var i = result.length - 1; i >= 0; i--) {
            if (this.isUserID(data[i]["user_id"])) {
              this.isShowApply = false;
            }
          }
          if (result.length > 0) {
            this.isShowAccept = true;
          }
        } else if (this.isUserID(this.project_user_id)) {
          //Owner => see all
          this.COPIs.push(result);
          this.isShowApply = false;
          if (result.length > 0) {
            this.isShowAccept = true;
          }
        } //not Owner => Only see owner apply, show apply btn if not apply
        else {
          this.isShowApply = true;
          this.isShowAccept = false;
          for (i = result.length - 1; i >= 0; i--) {
            if (this.isUserID(data[i]["user_id"])) {
              var temp = data[i];
              this.COPIs.push({ temp });
              this.isShowApply = false;
            }
          }
        }
        //over apply end date
        var now = new Date();
        if (this.apply_copi_end_date < this.dateFormat(now)) {
          this.isShowApply = false;
          this.activeColor = "red";
        }
      });
    }),
      getAllResearch().then((response) => {
        const exp_data = response.data;
        var i = 0;
        for (i = 0; i < exp_data.length; i++) {
          this.exp.push(exp_data[i]);
        }
      });
  },
  methods: {
    dateFormat(time) {
      var date = new Date(time.toString().replace(/-/g, "/"));
      var year = date.getFullYear();
      var month =
        date.getMonth() + 1 < 10
          ? "0" + (date.getMonth() + 1)
          : date.getMonth() + 1;
      var day = date.getDate() < 10 ? "0" + date.getDate() : date.getDate();
      return year + "-" + month + "-" + day;
    },

    btnApply() {
      this.isApplyDisabled = true;
      newCOPIProject(
        window.location.hash.split("/")[2],
        this.form.COPI_project_content
      )
        .then((response) => {
          if (response.status == "error") {
            throw new Error(response.message);
          }
          alert("Send COPI Apply Success.");
          window.location.reload();
        })
        .catch((error) => {
          alert("Send COPI Apply Error:" + error.message);
          console.log(error);
          window.location.reload();
          this.isApplyDisabled = false;
        })
        .finally(function () {
          this.isApplyDisabled = false;
        });
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
    btnAccept() {
      this.isDisabled = true;
      this.success_count = 0;
      for (var i = this.COPIs[0].length - 1; i >= 0; i--) {
        var COPI = this.COPIs[0];
        editCOPIAccepted(COPI[i].id, COPI[i].accepted)
          .then((response) => {
            if (response.status == "error") {
              throw new Error(response.message);
            }
            this.success_count = this.success_count + 1;
            if (this.success_count == this.COPIs[0].length) {
              alert("Accept Success!");
              window.location.reload();
            }
          })
          .catch((error) => {
            alert("Accept Error: " + error.message);
            console.log(error);
            window.location.reload();
            this.isDisabled = false;
          })
          .finally(function () {
            this.isDisabled = false;
          });
      }
    },
  },
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style scoped>
#collapse-1 {
  margin: 25px;
}
.applyBtn {
  /* margin-left: 100px; */
  margin-bottom: 30px;
}
.formBox {
  padding: 20px;
}
</style>
