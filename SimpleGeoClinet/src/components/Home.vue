<template>
    <v-container class="home">
        <p> Welcome to your new single-page application, built with <a href="https://vuejs.org" target="_blank" >Vue.js</a>
            and
            <a href="http://www.typescriptlang.org/" target="_blank">TypeScript</a>.
        </p>
        <v-card>
            <v-card-title class="pb-0">GeoServer Client</v-card-title>
            <v-form @submit.prevent="onSubmit">
                <v-card-text>
                    <v-text-field v-model="bBox" label="Bounding Box"></v-text-field>
                    <v-text-field v-model="styles" label="Styles"></v-text-field>
                    <v-text-field v-model="format" label="Format"></v-text-field>
                    <v-select v-model="request" :items="['GetMap', 'GetCapabilities']" label="Request"></v-select>
                    <v-text-field v-model="layers" label="Layers" hint="Please enter values divided by commas"></v-text-field>
                    <v-text-field v-model="width" label="Width"></v-text-field>
                    <v-text-field v-model="height" label="Height"></v-text-field>
                    <v-text-field v-model="srs" label="SRS"></v-text-field>
                </v-card-text>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn text color="primary" type="submit">Send request</v-btn>
                </v-card-actions>
            </v-form>
        </v-card>
    </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import axios from "axios";

@Component
export default class Home extends Vue {
    bBox: string = "540631.6237364038,120484.86830455417,570631.7865026393,165485.0310707898";
    styles: string = "";
    format: string = "image/png";
    request: string = "GetMap";
    layers: string = "gis:P100004,gis:P100051,gis:P100052";
    width: number = 767;
    height: number = 768;
    srs: string = "XXX"

    async onSubmit() {
        try {
            let res = await axios.get(
                `http://127.0.0.1:5000/geoserver/gis/wms`,
                {
                    params: {
                        BBOX: this.bBox,
                        STYLES: this.styles,
                        FORMAT: this.format,
                        REQUEST: this.request,
                        LAYERS: this.layers,
                        WIDTH: this.width,
                        HEIGHT: this.height,
                        SRS: this.srs,
                    }
                }
            );
            console.log(res);
        } catch (e) {
            console.log(e);
        }
    }
}
</script>
