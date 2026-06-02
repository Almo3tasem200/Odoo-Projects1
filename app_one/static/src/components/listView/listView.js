/* @odoo-module */

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class ListViewAction extends Component {
    static template = "app_one.ListView";

    setup(){
        this.state = useState({
            'records': []
        });
        this.orm = useService("orm"); // object relational mapping
        this.rpc = useService("rpc"); // remote procedure call
        this.loadRecords();
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
}

registry.category("actions").add("app_one.action_list_view", ListViewAction);