
openerp.nstda_gnc = function(instance){
	
	var MODELS_TO_HIDE = ['nstda.ctf.list.test.unit'];
	
	var QWeb = instance.web.qweb,
        _t  = instance.web._t,
        _lt = instance.web._lt;
	var dateBefore = null;
	
	/*
	instance.web.form.FieldBinaryFile.include({
        set_filename: function(value) {
            var filename = this.node.attrs.filename;
            var n = filename.indexOf(",");
            var tmp = {};
            
            if (n == -1){
            	if (filename) {
                    tmp[filename] = value;
                    this.field_manager.set_values(tmp);
                }
            }else{
            	var res = filename.split(",");
            	for (i = 0; i < res.length; i++) { 
            		if (res[i]) {
	            		tmp[res[i]] = value;
	            		this.field_manager.set_values(tmp);
            		}
            	}
            }
        },
        
    });
	
	*/
}