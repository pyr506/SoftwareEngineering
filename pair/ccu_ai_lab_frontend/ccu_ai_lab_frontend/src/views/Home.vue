<template>
  <div class="overflow-auto">
    <div class="text-center pageTitle">
      <h3 class="index_title">Latest News</h3>
    </div>
    <br />
    <NewsList :fields="fields" :items="items"></NewsList>
  </div>
</template>

<script>
import { getNews } from "../service/api.js";
import NewsList from "../components/NewsList.vue";

export default {
  components: { NewsList },
  data() {
    return {
      fields: [],
      fieldsAdmin: [
        { key: "Title", label: "Title"},
        { key: "Clicked", label: "Clicked"},
        { key: "DateTime(GMT)", label: "DateTime(GMT)"},
        { key: "Admin", label: "Admin"}
      ],
      
      fieldsUser: [
        { key: "Title", label: "Title"},
        { key: "Clicked", label: "Clicked"},
        { key: "DateTime(GMT)", label: "DateTime(GMT)"}
      ],
      items: [],
      user: localStorage.getItem("role_id")
    };
  },
  computed: {
    rows() {
      return this.items.length;
    }
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
    getFields() {
      if (this.isAdmin())
      {
        this.fields = this.fieldsAdmin;
      }
      else
      {
        this.fields = this.fieldsUser;
      }
    }
  },
  created() {
    getNews().then(response => {
      const data = response.data;
      var result = data
      for (var i = result.length-1; i>=0 ; i--)
      {
        this.items.push({ news_id: data[i]['id'], news_title: data[i]['title'], clicked: data[i]['clicked'], created_at: data[i]['created_at']} );
      }
    });
    this.getFields();
  }
};
</script>

<style>
.hidden_header {
  display: none;
}
.index_title {
    text-align: center;
    font-weight: bold;
    font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;

  }
.pageTitle {
  border-bottom: 2px solid #ffcf56;
  padding-bottom: 10px;
  margin-bottom: 20px;
  max-width: 10em;
  margin: auto;
}
</style>
