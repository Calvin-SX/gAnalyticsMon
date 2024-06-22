import {LitElement, html} from 'https://cdn.jsdelivr.net/gh/lit/dist@3/core/lit-core.min.js';

class UrlTable extends LitElement {
    static properties = {
        blacklistWebs: [],
        urls: [],
    };
    constructor() {
        super();
        this.getBlacklistWes();
    }
    getBlacklistWes() {
        const baseUrl = "/urls";
        fetch(baseUrl).then((response) => response.json()).then((jsonData) =>{
            this.blacklistWebs = jsonData;
        });
    }
    render() {
        return html`
            <p>
            <table>
                <tr>
                    <th>index</th>
                    <th>Blacklist webs</th>
                    <th>Select</th>
                </tr>
                ${this.blacklistWebs.map((item, idx)=>html`
                    <tr>
                        <td>${idx}</td>
                        <td>${item}</td>
                        <td><input type="checkbox" id="${idx}" unchecked/></td>
                    </tr>
                    `)}
            </table>
            </p>
        `
    }
}

customElements.define('url-table', UrlTable)