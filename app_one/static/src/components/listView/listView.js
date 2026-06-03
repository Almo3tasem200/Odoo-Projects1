/* @odoo-module */

import { Component, useState, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { FormView } from "@app_one/components/formView/formView"

export class ListViewAction extends Component {
    static template = "app_one.ListView";
    static components = { FormView }

    setup(){
        this.state = useState({
            'records': []
        });
        this.orm = useService("orm"); // object relational mapping
        this.rpc = useService("rpc"); // remote procedure call
        this.loadRecords();

        this.intervalId = setInterval(() => {this.loadRecords();}, 3000); //in 3000ms=3s render this function
        onWillUnmount(() => {
            clearInterval(this.intervalId);
            console.log("interval cleared")
        });

        this.onRecordCreated =this.onRecordCreated.bind(this);
    };

    // async loadRecords() {
    //   const result = await this.orm.searchRead("property", [], []); // model,domain,fields
    //   console.log(result);
    //   this.state.records = result;
    // };
    async loadRecords() {
      const result = await this.rpc("/web/dataset/call_kw", {
          model: "property",
          method: "search_read",
          args: [[]],
          kwargs: {
              fields: [
                  'id', 'name', 'postcode', 'date_availability'
              ]
          },
      });
      console.log(result);
      this.state.records = result;
    }; // function call

    async createRecord() {
        await this.rpc("/web/dataset/call_kw", {
            model: "property",
            method: "create",
            args: [{
                name: "new property",
                postcode: "1425482",
                date_availability: "2025-05-24"
            }],
            kwargs: {},
        })

        this.loadRecords();
    };
    async deleteRecord(recordId){
        await this.rpc("/web/dataset/call_kw", {
            model: "property",
            method: "unlink",
            args: [recordId],
            kwargs: {},
        });
        this.loadRecords();
    };

    toggleCreateForm(){
        console.log("inside toggleCreateForm");
        this.state.showCreateForm = !this.state.showCreateForm;
        console.log(this.state.showCreateForm);

    }

    onRecordCreated() {
        this.loadRecords();
        this.state.showCreateForm = false;
    }
}



registry.category("actions").add("app_one.action_list_view", ListViewAction);