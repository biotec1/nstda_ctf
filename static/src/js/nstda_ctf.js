openerp.nstda_ctf = function(instance) {

	var MODELS_TO_HIDE = [ 'nstda.ctf.list' ];
	var QWeb = instance.web.qweb, _t = instance.web._t, _lt = instance.web._lt;
	var dateBefore = null;

	instance.web.ListView
			.include({
				start : function() {
					var self = this;
					var ret = this._super.apply(this, arguments);
					var res_model = this.dataset.model;
					
					if ($.inArray(res_model, MODELS_TO_HIDE) != -1) {
						if (instance.webclient) {
							instance.webclient.menu.do_reload_needaction();
						}
					}
					;
					return ret;
				},

				load_list : function() {
					var self = this;
					var tmp = this._super.apply(this, arguments);
					var res_model = this.dataset.model;
					if ($.inArray(res_model, MODELS_TO_HIDE) != -1) {
						self.options.importable = false;
						$(".oe_selectcreatepopup-search-create").remove();
					}
					;
				},

				on_loaded : function(data, grouped) {
					// tree/@editable takes priority on everything else if
					// present.
					return this._super(data, grouped);
				},
			});

}