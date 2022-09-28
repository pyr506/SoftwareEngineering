<template>
  <div>
    <div class="text-right admin-link" v-if="isAdmin()">
      Management:
      <router-link :to="`/add_event?from=events`" class="homeLink">Add Event</router-link>
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
            <router-link :to="{ name: 'EventPage', params:{id:data.item.event_id}}" class="link">{{ data.item.event_title }}</router-link>
          </template>
          <template v-slot:cell(Clicked)="data">{{ data.item.clicked }}</template>
          <template v-slot:cell(DateTime(GMT))="data">{{ data.item.created_at }}</template>
          <template v-slot:cell(Admin)="data" v-if="isAdmin()">
            <button @click="gotoEditPage(data.item.event_id)" class="btn btn-link">Edit</button>
            /
            <button class="btn btn-link" @click="delBtn(data.item.event_id)">Delete</button>
          </template>
          <template v-slot:table-colgroup="scope">
            <col
              v-for="field in scope.fields"
              :key="field.key"
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
import axios from "axios";
import { deleteEvent } from "../service/api.js";

export default {
  components: {},
  props: ["fields", "items"],
  data() {
    return {
      perPage: 10,
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
      this.$router.push(`/events/` + id);
    },
    gotoEditPage(id) {
      this.$router.push(`/events/edit/` + id);
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
      const msg = "Are your sure to delete the event?";
      if (confirm(msg) == true) {
        deleteEvent(id)
          .then((response) => {
            if (response.status == 'error')
            {
              throw new Error(response.message);
            }
            alert("Delete Event Success");
            window.location.reload();
          })
          .catch((error) => {
            alert("Delete Event Error:" + error);
          });
      }
    }
  }
};
</script>