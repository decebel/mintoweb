var CategoryViewModel = Backbone.Model.extend({
    initialize: function () {
        this.set("title", undefined);
        this.set("description", undefined);
        this.set("ruleType", undefined);
        this.set("mlFile", undefined);
        this.set("keywordList", undefined);
        this.set("titleHasError", false);
        this.set("typeHasError", false);
        this.set("keywordHasError", false);
        this.set("mlHasError", false);
        this.set("isValid", false);
    },
    setRuleType: function (event, context) {
        context.model.set("ruleType", context.ruleType)
    },
    isKeyword: function(arg){
        return this.get("ruleType") === keywordRuleTypeString;
    },
    isMl: function(arg){
        return this.get("ruleType") === mlRuleTypeString;
    },
    validateTitle(){
        var titleString = this.get("title");
        this.set("titleHasError", (!titleString || titleString === "")); 
    },
    validateRuleType(){
        var ruleType = this.get("ruleType");
        this.set("typeHasError", (ruleType !== keywordRuleTypeString && ruleType !== mlRuleTypeString));
    },
    validateKeywordList(){
        var ruleType = this.get("ruleType");
        if (ruleType === keywordRuleTypeString){
            var keywordList = this.get("keywordList");
            this.set("keywordHasError", (!keywordList || keywordList === ""));
            this.set("mlHasError", false);
        }
    },
    validateMlFile(){
        var ruleType = this.get("ruleType");
        if (ruleType === mlRuleTypeString){
            var mlFile = this.get("mlFile");
            this.set("mlHasError", (!mlFile || mlFile === "" || mlFile === "Select example text file"));
            this.set("keywordHasError", false);
        }
    },
    validate: function(attrs, options) {
        this.validateTitle();
        this.validateRuleType();
        this.validateKeywordList();
        this.validateMlFile();
        this.set("isValid", (!this.get("titleHasError") &&
                             !this.get("typeHasError") &&
                             !this.get("keywordHasError") &&
                             !this.get("mlHasError")));
        return(this.get("isValid"));
  }
});

var newCategoryViewModel;

$(document).ready(function () {
    resetNewCategoryViewModel();
});

function createNewRule() {
    addedCategories.push(newCategoryViewModel.get("title"));
    viewmodel.refresh();
}

function resetNewCategoryViewModel() {
    if (newCategoryViewModel){
        // To reset the form fields
        newCategoryViewModel.initialize();
    }
    newCategoryViewModel = new CategoryViewModel();
    
    $("#createNewRuleModal").modal("hide");
    rivets.bind($("#createNewRuleModal"), { model: newCategoryViewModel });
    newCategoryViewModel.on("change:title", function() {
        newCategoryViewModel.validateTitle();
    });
    newCategoryViewModel.on("change:ruleType", function() {
        newCategoryViewModel.validateRuleType();
    });
    newCategoryViewModel.on("change:mlFile", function() {
        newCategoryViewModel.validateMlFile();
    });
    newCategoryViewModel.on("change:keywordList", function() {
        newCategoryViewModel.validateKeywordList();
    });
}

function validateForm(){
    var isValid = newCategoryViewModel.validate();
    if (isValid){
        createNewRule();
        resetNewCategoryViewModel();
    }
    // to prevent postback
    return false;
}

function onFileChanged(){
    var fileName = $("input.upload")[0].value;
    newCategoryViewModel.set("mlFile", fileName);
}

