<template>
    <v-app>
        <v-app-bar app color="primary" dark></v-app-bar>

        <v-content>
            <Home />
        </v-content>
    </v-app>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import Home from "./components/Home.vue";

@Component({
    components: {
        Home
    }
})
export default class App extends Vue {}
</script>
