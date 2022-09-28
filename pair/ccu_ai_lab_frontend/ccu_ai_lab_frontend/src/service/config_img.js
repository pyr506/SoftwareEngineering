import axios from 'axios'
export const Config = {
  headers: {
    'content-type': 'multipart/form-data',
  },
  timeout: 10000,
  withCredentials: true,
  responseType: 'json',
}

const service_img = axios.create({
  baseURL: 'https://127.0.0.1:5000/api/v1',
  timeout: Config.timeout,
  headers: Config.headers,
  responseType: Config.responseType,
})

service_img.interceptors.request.use(
  config => {
    config.headers['content-type'] = 'multipart/form-data';
    if (localStorage.getItem('token') != null) {
      config.headers['x-access-tokens'] = localStorage.getItem('token');
    }
    console.log(config)
    return config;
  },
  error => {
    console.log(error);
    return Promise.reject(error);
  }
)

service_img.interceptors.response.use(
  res => {
    if (res.data.status == 'error') {
      if (res.data.message == "Token is invalid" || res.data.message == "Access Denied, Please Login First.") {
        localStorage.removeItem("token");
        localStorage.removeItem("id");
        localStorage.removeItem("username");
        localStorage.removeItem("role_id");
        this.$store.state.isLogin = false;
        window.location.replace("/");
      }
    }
    if (res.status === 200) {
      //delete action
      if (res.data == null) {
        return true;
      }
      return Promise.resolve(res.data);
    } else {
      return Promise.reject(res.message);
    }
  },
  error => {
    console.log(error.message)
    if (error.message == "Token is invalid" || error.message == "Access Denied, Please Login First.") {
      localStorage.removeItem("token");
      localStorage.removeItem("id");
      localStorage.removeItem("username");
      localStorage.removeItem("role_id");
      window.location.replace("/");
    }
    return Promise.reject(error);
  }
)

export default service_img;