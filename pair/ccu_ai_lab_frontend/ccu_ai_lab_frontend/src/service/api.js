import service from './config.js';
import service_img from './config_img.js';

export const send_error = (id) => {
	const params = {
		id: id
	};
	return service.post('/chat/reply_error', params);
};

export const echomsg = (msg, user_id, token) => {
  const params = {
    msg: msg,
    user_id: user_id,
    token: token
  };
  return service.post('/chat/get_response', params);
};

export const querymsg = (user_id,token) => {
  const params = {
    user_id: user_id,
    token: token
  };
  return service.post('/chat/get_record', params);
};

export const register = (email, username, password, confirm_password) => {
  const params = {
    email: email,
    username: username,
    password: password,
    confirm_password: confirm_password,
    role_id: 1,
  };
  return service.post('/auth/register', params);
};

export const confirmed_email = (user_id ,confirmed_hash) => {
  const params = {
    user_id: user_id,
    confirmed_hash: confirmed_hash,
  };
  return service.put('/auth/confirmed/', params);
};

export const login = (email, password) => {
  const params = {
    email: email,
    password: password,
  };
  return service.post('/auth/login', params);
};

export const resend = (email) => {
  const params = {
    email: email
  };
  return service.post('/auth/resend', params);
};

export const resetpassword = (email) => {
  const params = {
    email: email
  };
  return service.post('/auth/resetpassword', params);
};

export const getUser = (token) => {
  const params = {
    token: token,
  };
  return service.post('/auth/login', params);
};

export const logout = () => {
  const params = {};
  return service.delete('/auth/logout', {data: { foo: 'bar'}});
};

export const changePW = (password, new_password, confirm_password) => {
  const params = {
    password: password,
    new_password: new_password,
    confirm_password: confirm_password,
  };
  return service.put('/auth/change_password', params);
};

export const getNews = () => {
  return service.get('/news');
};

export const getNewsDetail = (id) => {
  return service.get(`/news/${id}`);
};

export const newNews = (title, content) => {
  const params = {
    title: title,
    content: content
  };
  return service.post('/news', params);
};

export const editNews = (id, title, content) => {
  const params = {
    title: title,
    content: content
  };
  return service.put(`/news/${id}`, params);
};

export const deleteNews = (id) => {
  try {
    return service.delete(`/news/${id}`, {data: { foo: 'bar'}});
  }
  catch (error)
  { throw new Error(error);}
};

export const getEvents = () => {
  return service.get('/events');
};

export const getEventDetail = (id) => {
  return service.get(`/events/${id}`);
};

export const newEvent = (title, content) => {
  const params = {
    title: title,
    content: content
  };
  return service.post('/events', params);
};

export const editEvent = (id, title, content) => {
  const params = {
    title: title,
    content: content
  };
  return service.put(`/events/${id}`, params);
};

export const deleteEvent = (id) => {
  try {
    return service.delete(`/events/${id}`, {data: { foo: 'bar'}});
  }
  catch (error)
  { throw new Error(error);}
};

export const getUserInfo = (id) => {
  return service.get(`/users/${id}`);
};

export const getUsers = () => {
  return service.get('/users');
};

export const blockuser = (id) => {
  try {
    return service.delete(`/users/${id}`, {data: { foo: 'bar'}});
  }
  catch (error)
  { throw new Error(error);}
};

export const editUser = (
  id,
  email,
  first_name,
  last_name,
  username,
  country,
  company,
  job_title,
  about_me,
  confirmed,
  blocked,
  researches
) => {
  const researches_dict = [];
  const researches_name_dict = [];
  var i = 0;
  for (i = 0; i < researches.length; i++) {
    researches_dict.push(researches[i].id);
    researches_name_dict.push(researches[i].name);
  }
  
  const params = {
    email: email,
    first_name: first_name,
    last_name: last_name,
    username: username,
    country: country,
    company: company,
    job_title: job_title,
    about_me: about_me,
    confirmed: confirmed,
    blocked: blocked,
    researches: researches_dict,
    researches_name: researches_name_dict
  };
  return service.put(`/users/${id}`, params);
};

export const getAllResearch = () => {
  return service.get(`/researches`);
};

export const getSelfProject = (id) => {
  return service.get(`/specific_periods/${id}`);
};

export const getAllProject = () => {
  return service.get(`/specific_periods`);
};

export const getMyProject = () => {
  return service.get(`/specific_periods/myproject`);
};

export const getMyCOPIProjects = () => {
  return service.get(`/specific_periods/myCOPIproject`);
};

export const getInterestingProjects = () => {
  return service.get(`/specific_periods/interesting_project`);
};

export const newProject = (
  input_researches,
  country,
  university,
  name_of_pi,
  department,
  project_title,
  link,
  start_date,
  end_date,
  apply_copi_end_date,
  project_content
) => {
  const user_researches_array = [];
  const user_researches_name_array = [];
  var k = 0;
  for (k = 0; k < input_researches.length; k++) {
    user_researches_array.push(input_researches[k].id);
    user_researches_name_array.push(input_researches[k].name);
  }
  const params = {
    researches: user_researches_array,
    researches_name: user_researches_name_array,
    country: country,
    university: university,
    name_of_pi: name_of_pi,
    department: department,
    project_title: project_title,
    link: link,
    start_date: start_date,
    end_date: end_date,
    apply_copi_end_date: apply_copi_end_date,
    project_content: project_content
  };
  return service.post(`/specific_periods`, params);
};

export const editProject = (
  project_id,
  input_researches,
  country,
  university,
  name_of_pi,
  department,
  project_title,
  link,
  start_date,
  end_date,
  apply_copi_end_date,
  project_content
) => {
  const user_researches_array = [];
  const user_researches_name_array = [];
  var k = 0;
  for (k = 0; k < input_researches.length; k++) {
    user_researches_array.push(input_researches[k].id);
    user_researches_name_array.push(input_researches[k].name);
  }
  const params = {
    researches: user_researches_array,
    researches_name: user_researches_name_array,
    country: country,
    university: university,
    name_of_pi: name_of_pi,
    department: department,
    project_title: project_title,
    link: link,
    start_date: start_date,
    end_date: end_date,
    apply_copi_end_date: apply_copi_end_date,
    project_content: project_content
  };
  return service.put(`/specific_periods/${project_id}`, params);
};

export const deleteProject = (id) => {
  return service.delete(`/specific_periods/${id}`, {data: { foo: 'bar'}});
};

export const newCOPIProject = (project_id, COPI_project_content) => {
  try{
    const params = {
      project_id: project_id,
      COPI_project_content: COPI_project_content
    };
    return service.post('/COPI_projects', params);
  } 
  catch (error)
  {
    throw new Error(error);
  }
  
};

export const getCOPIProjects = (project_id) => {
  return service.get(`/COPI_projects/${project_id}`);
};

export const editCOPIAccepted = (COPI_id, accepted) => {
  const params = {
    accepted: accepted,
  };
  return service.put(`/COPI_projects/${COPI_id}`, params);
};

export const getWebinfos = () => {
  return service.get('/webinfos');
};

export const editWebinfos = (tel, email, address) => {
  const params = {
    tel: tel,
    email: email,
    address: address
  };
  return service.put(`/webinfos`, params);
};

export const uploadImage = (blob) => {
  let formdata = new FormData();
  formdata.append("file", blob);
  return service_img.post(`/imageuploader`, formdata);
}
