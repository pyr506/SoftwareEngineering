<template>
  <div>
    <h2>
      <strong>▹ {{ title }}</strong>
    </h2>
    <hr />

    <div class="contentBox">
      <TinymceViewer ref="editor"
        v-model="content"
      >
      </TinymceViewer>
    </div>

    <div class="text-right post-detail">
      <div>Clicked: {{ clicked }}</div>
      <div>Created Date (GMT):{{ created_at }}</div>
      <div>Updated Date (GMT):{{ updated_at }}</div>
    </div>
    <div class="text-right contentBox">
      <b-button pill variant="outline-secondary" @click="$router.go(-1)">back</b-button>
    </div>
  </div>
</template>
<script>
import { getNewsDetail } from "../../service/api.js";
import TinymceViewer from '../../components/TinymceViewer.vue'
export default {
  components: {
    TinymceViewer
  },
  data() {
    return {
      title: "",
      content: "",
      clicked: "",
      created_at: "",
      updated_at: ""
    };
  },

  created() {
    getNewsDetail(window.location.hash.split("/")[2]).then(response => {
      this.title = response.data.title;
      this.content = response.data.content;
      this.clicked = response.data.clicked;
      this.created_at = response.data.created_at;
      this.updated_at = response.data.updated_at;
    });
  }
};
</script>
