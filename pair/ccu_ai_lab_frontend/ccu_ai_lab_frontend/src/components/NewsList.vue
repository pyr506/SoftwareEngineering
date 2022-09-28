<template>
  <div>
    <div class="text-right admin-link" v-if="isAdmin()">
      Management:
      <router-link :to="`/add_news?from=news`" class="homeLink">Add News</router-link>
    </div>
    <template>
      <div>
        <b-table
          :fields="fields"
          :items="items"
          :per-page=10
          :current-page="currentPage"
        >
          <template v-slot:cell(Title)="data">
            <router-link :to="{ name: 'NewsPage', params:{id:data.item.news_id}}" class="link">{{ data.item.news_title }}</router-link>
          </template>
          <template v-slot:cell(Clicked)="data">{{ data.item.clicked }}</template>
          <template v-slot:cell(DateTime(GMT))="data">{{ data.item.created_at }}</template>
          <template v-slot:cell(Admin)="data" v-if="isAdmin()" >
            <button  @click="gotoEditPage(data.item.news_id)" class="btn btn-link">Edit</button>
            /
            <button class="btn btn-link" @click="delBtn(data.item.news_id)">Delete</button>
          </template>
          <template v-slot:table-colgroup="scope">
              <col
                v-for="field in scope.fields"
                :key="field.key"
                :style="{ width: field.key === 'Clicked' ? '50px': ''}"
              />
          </template>
        </b-table>
        <b-pagination
          v-model="currentPage"
          :total-rows="rows"
          :per-page=10
          aria-controls="my-table"
          align="right"
        ></b-pagination>
      </div>
    </template>
  </div>
</template>

<script>
import { deleteNews } from "../service/api.js";

export default {
  components: {},
  props: ["fields", "items"],
  data() {
    return {
      currentPage: 1,
      user: localStorage.getItem("role_id")
    };
  },
  computed: {
    rows() {
      return this.items.length;
    }
  },
  methods: {
    gotoPage(id) {
      this.$router.push(`/news/` + id);
    },
    gotoEditPage(id) {
      this.$router.push(`/news/edit/` + id);
    },
    isAdmin() {
      if (this.user == 3) {
        return true;
      }
      else
      {
        return false;
      }
    },
    delBtn(id) {
      const msg = "Are your sure to delete the news?";
      if (confirm(msg) == true) {
        deleteNews(id)
          .then((response) => {
            if (response.status == 'error')
            {
              throw new Error(response.message);
            }
            alert("Delete News Success");
            window.location.reload();
          })
          .catch((error) => {
            alert("Delete News Error:" + error);
          });
      }
    }
  }
};
</script>