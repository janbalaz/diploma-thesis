<template>
  <b-navbar toggleable="md" type="dark" variant="info" class="nav">
    <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
    <b-navbar-brand><router-link to="/" class="nav-link">NAMEOFAPP</router-link></b-navbar-brand>
    <b-collapse is-nav id="nav_collapse">
      <b-navbar-nav>
        <li class="nav-item"><router-link to="/" class="nav-link">Home</router-link></li>
        <li class="nav-item"><router-link to="/topics" class="nav-link">Topics</router-link></li>
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-item-dropdown text="Model" right>
          <b-dropdown-item href="#">LDA</b-dropdown-item>
          <b-dropdown-item href="#">LSA</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>

    </b-collapse>
  </b-navbar>
</template>

<script>
  export default {
    name: 'Navbar',
    data () {
      return {
        name: 'Welcome to Your Vue.js App'
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .nav {
    margin-bottom: 20px;
  }
  .bg-info {
    background-color: #343a40 !important;
  }
  .navbar-brand > a {
    color: #FFF;
  }
</style>
