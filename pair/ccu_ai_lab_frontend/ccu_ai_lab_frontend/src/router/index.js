import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Chat from "../views/Chat.vue";
import News from "../views/News.vue";
import Events from "../views/Events.vue";
import About from "../views/About.vue";
import Login from "../views/Login.vue";
import ForgetPassword from "../views/ForgetPassword.vue";
import Members from "../views/Members.vue";
import Register from "../views/Register.vue";
import RegisterForm from "../views/RegisterForm.vue";
import RegisterResend from "../views/RegisterResend.vue";
import ConfirmedEmail from "../views/ConfirmedEmail.vue";
import Contact from "../views/Contact.vue";
import MyAccount from "../views/MyAccount.vue";
import MyAccountInfo from "../views/MyAccountInfo.vue";
import MyAccountPW from "../views/MyAccountPW.vue";
import Users from "../views/Users.vue";
import UserPage from "../views/pages/UserPage.vue";
import EditUser from "../views/pages/EditUserPage.vue";
import AddProject from "../views/AddProject.vue";
import Projects from "../views/Projects.vue";
import ProjectPage from "../views/pages/ProjectPage.vue";
import EditProjectPage from "../views/pages/EditProjectPage.vue";
import NewsPage from "../views/pages/NewsPage.vue";
import EditNewsPage from "../views/pages/EditNewsPage.vue";
import AddNews from "../views/AddNews.vue";
import EventPage from "../views/pages/EventPage.vue";
import EditEventPage from "../views/pages/EditEventPage.vue";
import AddEvent from "../views/AddEvent.vue";
import EditWebinfos from "../views/pages/EditWebinfos.vue";
import Help from "../views/Help.vue";

Vue.use(VueRouter);
const baseRouter = '/center'
const routes = [{
  path: "/",
  name: "Home",
  component: Home,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - Home",
  }
}, {
  path: "/news",
  name: "News",
  component: News,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - News",
  }
}, {
  path: "/news/:id",
  name: "NewsPage",
  component: NewsPage,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - News"
  }
}, {
  path: "/news/edit/:id",
  name: "Edit the News",
  component: EditNewsPage,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - Edit the News"
  }
},{
  path: "/events",
  name: "Events",
  component: Events,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - Events"
  }
}, {
  path: "/events/:id",
  name: "EventPage",
  component: EventPage,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - Event"
  }
}, {
  path: "/events/edit/:id",
  name: "Edit the Event",
  component: EditEventPage,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - Edit the Evnet"
  }
}, {
  path: "/about",
  name: "About",
  component: About,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - About us"
  }
}, {
  path: "/login",
  name: "Login",
  component: Login,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - Login"
  }
}, {
  path: "/forgetpassword",
  name: "Forget Password",
  component: ForgetPassword,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - Forget Password"
  }
},{
  path: "/members",
  name: "Members",
  component: Members,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - Members"
  }
}, {
  path: "/register",
  name: "Register rules",
  component: Register,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - Register rules"
  }
}, {
  path: "/register-form",
  name: "Register",
  component: RegisterForm,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - Register"
  }
}, {
  path: "/register-resend",
  name: "RegisterResend",
  component: RegisterResend,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - Register Resend"
  }
}, {
  path: "/auth/confirmed/:id/:confirmed_email",
  name: "Confirmed Email",
  component: ConfirmedEmail,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - Confirmed Email"
  }
}, {
  path: "/users",
  name: "Users",
  component: Users,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - Users"
  }
}, {
  path: "/users/:id",
  name: "UserPage",
  component: UserPage,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - user"
  }
}, {
  path: "/users/edit/:id",
  name: "Edit the User",
  component: EditUser,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - Edit the User"
  }
}, {
  path: "/projects",
  name: "Projects",
  component: Projects,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - Projects"
  }
}, {
  path: "/projects/edit/:id",
  name: "Edit the Project",
  component: EditProjectPage,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - Edit the Project"
  }
}, {
  path: "/contact",
  name: "Contact",
  component: Contact
}, {
  path: "/my_account",
  name: "My Account",
  component: MyAccount,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - My Account"
  }
}, {
  path: "/my_account_info",
  name: "Change Personal Information",
  component: MyAccountInfo,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - Change Personal Information"
  }
}, {
  path: "/my_account_password",
  name: "Change Password",
  component: MyAccountPW,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - Change Password"
  }
}, {
  path: "/add_project",
  name: "Add Project",
  component: AddProject,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - Add Project"
  }
}, {
  path: "/projects/:id",
  name: "ProjectPage",
  component: ProjectPage,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - Project"
  }
}, {
  path: "/add_news",
  name: "Add News",
  component: AddNews,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - Add News"
  }
}, {
  path: "/add_event",
  name: "Add Event",
  component: AddEvent,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - Add Event"
  }
}, {
  path: "/webinfos/edit/",
  name: "Edit Webinfos",
  component: EditWebinfos,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - Edit Webinfos"
  }
}, {
  path: "/help",
  name: "Help",
  component: Help,
  meta: {
    title: "Taiwan-India Professional Expertise and Organization Cooperation Platform - Help"
  }
},
];

const router = new VueRouter({
  mode: "",
  base: process.env.BASE_URL,
  routes
});

// This callback runs before every route change, including on page load.
router.beforeEach((to, from, next) => {
  // This goes through the matched routes from last to first, finding the closest route with a title.
  // e.g., if we have `/some/deep/nested/route` and `/some`, `/deep`, and `/nested` have titles,
  // `/nested`'s will be chosen.
  const nearestWithTitle = to.matched.slice().reverse().find(r => r.meta && r.meta.title);

  // Find the nearest route element with meta tags.
  const nearestWithMeta = to.matched.slice().reverse().find(r => r.meta && r.meta.metaTags);

  // If a route with a title was found, set the document (page) title to that value.
  if(nearestWithTitle) document.title = nearestWithTitle.meta.title;

  // Remove any stale meta tags from the document using the key attribute we set below.
  Array.from(document.querySelectorAll('[data-vue-router-controlled]')).map(el => el.parentNode.removeChild(el));

  // Skip rendering meta tags if there are none.
  if(!nearestWithMeta) return next();

  // Turn the meta tag definitions into actual elements in the head.
  nearestWithMeta.meta.metaTags.map(tagDef => {
    const tag = document.createElement('meta');

    Object.keys(tagDef).forEach(key => {
      tag.setAttribute(key, tagDef[key]);
    });

    // We use this to track which meta tags we create so we don't interfere with other ones.
    tag.setAttribute('data-vue-router-controlled', '');

    return tag;
  })
  // Add the meta tags to the document head.
  .forEach(tag => document.head.appendChild(tag));

  next();
});

export default router;