 this.ckan.module('image-upload-cropper', function($) {
  return {
    /* options object can be extended using data-module-* attributes */
    options: {
      is_url: false,
      is_upload: false,
      field_upload: 'image_upload',
      field_url: 'image_url',
      field_clear: 'clear_upload',
      field_name: 'name',
      upload_label: '',
      previous_upload: false,
      // vars to store data the cropper needs
      cropper: null,
      canvas: null,
      file: null,
      self: null,
    },

    /* Should be changed to true if user modifies resource's name
     *
     * @type {Boolean}
     */
    _nameIsDirty: false,

    /* Initialises the module setting up elements and event listeners.
     *
     * Returns nothing.
     */
    initialize: function () {
      $.proxyAll(this, /_on/);
      var options = this.options;

      // firstly setup the fields
      var field_upload = 'input[name="' + options.field_upload + '"]';
      var field_url = 'input[name="' + options.field_url + '"]';
      var field_clear = 'input[name="' + options.field_clear + '"]';
      var field_name = 'input[name="' + options.field_name + '"]';

      this.input = $(field_upload, this.el);
      this.field_url = $(field_url, this.el).parents('.form-group');
      this.field_image = this.input.parents('.form-group');
      this.field_url_input = $('input', this.field_url);
      this.field_name = this.el.parents('form').find(field_name);
      // this is the location for the upload/link data/image label
      this.label_location = $('label[for="field-image-url"]');
      // determines if the resource is a data resource
      this.is_data_resource = (this.options.field_url === 'url') && (this.options.field_upload === 'upload');
      this.previousUpload = this.options.previous_upload;

      // Is there a clear checkbox on the form already?
      var checkbox = $(field_clear, this.el);
      if (checkbox.length > 0) {
        checkbox.parents('.form-group').remove();
      }

      // Adds the hidden clear input to the form
      this.field_clear = $('<input type="hidden" name="' + options.field_clear +'">')
        .appendTo(this.el);

      // Button to set the field to be a URL
      this.button_url = $('<a href="javascript:;" class="btn btn-default">' +
                          '<i class="fa fa-globe"></i>' +
                          this._('Link') + '</a>')
        .prop('title', this._('Link to a URL on the internet (you can also link to an API)'))
        .on('click', this._onFromWeb)
        .insertAfter(this.input);

      // Button to attach local file to the form
      this.button_upload = $('<a href="javascript:;" class="btn btn-default" id="btn-select-image">' +
                             '<i class="fa fa-cloud-upload"></i>' +
                             this._('Select image') + '</a>')
        .insertAfter(this.input);

      if (this.previousUpload) {
        $('<div class="error-inline"><i class="fa fa-warning"></i> ' +
          this._('Please select the file to upload again') + '</div>').appendTo(this.field_image);
      }

      // Button for resetting the form when there is a URL set
      var removeText = this._('Remove');
      $('<a href="javascript:;" class="btn btn-danger btn-remove-url">'
        + removeText + '</a>')
        .prop('title', removeText)
        .on('click', this._onRemove)
        .insertBefore(this.field_url_input);

      // Update the main label (this is displayed when no data/image has been uploaded/linked)
      $('label[for="field-image-upload"]').text(options.upload_label || this._('Image'));

      // Setup the file input
      this.input
        .on('mouseover', this._onInputMouseOver)
        .on('mouseout', this._onInputMouseOut)
        .on('change', this._onInputChange)
        .prop('title', this._('Upload a file on your computer'))
        .prop('accept', '.jpg, .jpeg, .png')
        .css('width', this.button_upload.outerWidth());

      // Fields storage. Used in this.changeState
      this.fields = $('<i />')
        .add(this.button_upload)
        .add(this.button_url)
        .add(this.input)
        .add(this.field_url)
        .add(this.field_image);

      // Disables autoName if user modifies name field
      this.field_name
        .on('change', this._onModifyName);
      // Disables autoName if resource name already has value,
      // i.e. we on edit page
      if (this.field_name.val()){
        this._nameIsDirty = true;
      }

      if (options.is_url) {
        this._showOnlyFieldUrl();

        this._updateUrlLabel(this._('URL'));
      } else if (options.is_upload) {
        this._showOnlyFieldUrl();

        this.field_url_input.prop('readonly', true);
        // If the data is an uploaded file, the filename will display rather than whole url of the site
        var filename = this._fileNameFromUpload(this.field_url_input.val());
        this.field_url_input.val(filename);

        this._updateUrlLabel(this._('File'));
      } else {
        this._showOnlyButtons();
      }
    },

    /* Quick way of getting just the filename from the uri of the resource data
     *
     * url - The url of the uploaded data file
     *
     * Returns String.
     */
    _fileNameFromUpload: function(url) {
      // If it's a local CKAN image return the entire URL.
      if (/^\/base\/images/.test(url)) {
        return url;
      }

      // remove fragment (#)
      url = url.substring(0, (url.indexOf("#") === -1) ? url.length : url.indexOf("#"));
      // remove query string
      url = url.substring(0, (url.indexOf("?") === -1) ? url.length : url.indexOf("?"));
      // extract the filename
      url = url.substring(url.lastIndexOf("/") + 1, url.length);

      return url; // filename
    },

    /* Update the `this.label_location` text
     *
     * If the upload/link is for a data resource, rather than an image,
     * the text for label[for="field-image-url"] will be updated.
     *
     * label_text - The text for the label of an uploaded/linked resource
     *
     * Returns nothing.
     */
    _updateUrlLabel: function(label_text) {
      if (! this.is_data_resource) {
        return;
      }

      this.label_location.text(label_text);
    },

    /* Event listener for when someone sets the field to URL mode
     *
     * Returns nothing.
     */
    _onFromWeb: function() {
      this._showOnlyFieldUrl();

      this.field_url_input.focus()
        .on('blur', this._onFromWebBlur);

      if (this.options.is_upload) {
        this.field_clear.val('true');
      }

      this._updateUrlLabel(this._('URL'));
    },

    /* Event listener for resetting the field back to the blank state
     *
     * Returns nothing.
     */
    _onRemove: function() {
      this._showOnlyButtons();
      this.field_url_input.val('');
      this.field_url_input.prop('readonly', false);
      this.field_clear.val('true');
      // remove the cropped img preview from the form in case the user will 
      // have another go at selecting/editing their image
      $('#form-img-preview-container').remove();
      if (this.options.cropper) {
        this.options.cropper.destroy();
      }
      this.options.cropper = null;
      // we don't need the canvas anymore
      this.options.canvas = null;
      this.options.file = null;
    },

   
    /* Event listener for when someone chooses a file to upload
     *
     * Returns nothing.
     */
    _onInputChange: function() {
      // remove error from DOM if it exists already from previous file selection
      $("#file-type-error").remove();
      var self = this;
      this.options.file = this.input[0].files[0];
      // we only accept these file types
      var validFileTypes = ["image/jpeg", "image/jpg", "image/png"];
      if ( this.options.file && validFileTypes.includes(this.options.file.type)) {
      var file_name = this.input.val().split(/^C:\\fakepath\\/).pop();

      // Internet Explorer 6-11 and Edge 20+
      var isIE = !!document.documentMode;
      var isEdge = !isIE && !!window.StyleMedia;
      // for IE/Edge when 'include filepath option' is enabled
      if (isIE || isEdge) {
        var fName = file_name.match(/[^\\\/]+$/);
        file_name = fName ? fName[0] : file_name;
      }
      this.field_url_input.val(file_name);
      this.field_url_input.prop('readonly', true);
      this.field_clear.val('');
      this._showOnlyFieldUrl();
      this._autoName(file_name);
      this._updateUrlLabel(this._('File'));

      //  Cropping related operations
      var reader = new FileReader();
      
      reader.onload = function(e) {
        self._showModalAndInitialiseCropper(e);
      }
      reader.readAsDataURL(this.options.file);
      reader.onerror = function(error) {
        $('<div id="file-type-error" class="error-inline"><i class="fa fa-warning"></i> ' +
        this._("Error reading file. Please try again.") + '</div>').appendTo(this.field_image);
      }
      } else {
        $('<div id="file-type-error" class="error-inline"><i class="fa fa-warning"></i> ' +
          this._("Invalid file type. Please select a .jpg, .jpeg, or .png file.") + '</div>').appendTo(this.field_image);
      }
    },

    _showModalAndInitialiseCropper: function(e) {
      if (!this.isEditing) {
        var imageUrl = e.target.result;
        $("#cropper-output-image").attr("src", imageUrl);
      } else {
        $("#cropper-output-image").attr("src", this.options.canvas.toDataURL());
      }
      // Open the modal
      $("#cropper-modal").modal("show");

      $("#cropper-modal").on("shown.bs.modal", () => {
        // Remove the backdrop-filter property as it conflicts with the modal-backdrop element 
        //  due to stacking contexts; this will probably change with a newer version of Bootstrap (3+)
        $('.row.wrapper').css('backdrop-filter', 'none');
        if (this.options.cropper !== null) {
          this.options.cropper.destroy();
        }
        // Initialize the cropper
        this._initializeCropper(e);
        
      });
      // Set click handlers for the "Apply" and "Cancel" buttons
      this._setModalButtonHandlers();
    },

    _initializeCropper: function(e) {
      var modalBodyWidth = $("#modal-cropper-body").width();
      var modalBodyHeight = $("#modal-cropper-body").height();
      this.options.cropper = new Cropper(document.getElementById("cropper-output-image"), {
        aspectRatio: 1,
        viewMode: 0,
        responsive: true,
        modal: false,
        minContainerHeight: 250,
        crop: function(event) {
          var canvas = this.cropper.getCroppedCanvas({
            width: modalBodyWidth * 0.5,
            height: modalBodyHeight * 0.5,
          });
          $("#preview").hide();
          $("#preview").attr('src', canvas.toDataURL("image/png"));
          $("#preview").show();
        }
      });
    },
    
    _setModalButtonHandlers: function() {
      $("#apply-crop").off("click").click(() => {
        this._handleApplyCrop();
      });
      
      $("#cancel-crop").off("click").click(() => {
        this._handleCancelCrop();
      });
      $('#zoom-in').off().click(() => {
        this.options.cropper.zoom(0.1); // Zoom in by 10%
      });
      
      $('#zoom-out').off().click(() => {
        this.options.cropper.zoom(-0.1); // Zoom out by 10%
      });
    },

    _handleApplyCrop: function() {
      // Because both Apply Crop and Cancel Crop button event handlers are closing the
      // modal, we need to keep track of when the Apply button was clicked so that 
      // we do not end up clearing the input on modal.hide() event handler
      this.applyClicked = true;
      this.options.canvas = this.options.cropper.getCroppedCanvas({
        width: 500,
        height: 500,
        // fillColor: "#ffffff"
      });
      this.options.canvas.toBlob((blob) => {
        // Create a new File object with the same name/type as the original file
        var newFile = new File([blob], this.options.file.name, {type: this.options.file.type});     
        // Replace the original file in the input element with the new File object
        this._replaceInputFile(newFile);
      }, this.options.file.type);
      // Close the modal
      $("#cropper-modal").modal("hide");
      $("#cropper-modal").on("hidden.bs.modal", () => {
        this._onModalHide();
      });
      // creates the div element to hold an img preview to show the user in the form,
      // plus adds the Edit button underneath with a click handler attached
      var imageUrl = this.options.canvas.toDataURL("image/png");
      var formImgPreview = 
      $('<img id="form-img-preview" style="height: 150px; width: 150px; border-radius: 4px; border: 2px solid var(--brand-colour-blue);" src="'
      + imageUrl + '" alt="Cropped Image preview" />');
      var editButton = $('<button class="btn btn-primary" type="button" id="crop-edit-btn">Edit</>');
      var formImgPreviewContainer = $('<div id="form-img-preview-container"><h6>Selected image preview</h6></div>');
      formImgPreviewContainer.append(formImgPreview);
      editButton.appendTo(formImgPreviewContainer);
      formImgPreviewContainer.appendTo(this.field_url);
      $("#crop-edit-btn").off("click").click(() => {
        this._handleEditCrop();
      })
    },

    _handleEditCrop: function() {
      this.isEditing = true;
      $('#form-img-preview-container').remove();
      this._showModalAndInitialiseCropper();
    },
    
    _handleCancelCrop: function() {
      this.applyClicked = false;
      this.isEditing = false;
      // we don't need to call modal.hide() here because the Cancel button has the
      // attribute data-dimiss already wich triggers bellow event
      $("#cropper-modal").on("hidden.bs.modal", () => {
        this._onModalHide();
      });
    },
    
    _replaceInputFile: function(newFile) {
      // Creates a new DataTransfer object because due to security reasons
      // we can't modify the Filelist of the file input field; it is read-only
      var dataTransfer = new DataTransfer();
      dataTransfer.items.add(newFile);
      // Replace the original file in the input element with the new File object
      this.input[0].files = dataTransfer.files;
    },

    /* Called on either clicking the Apply/Cancel buttons on the Cropping modal
     *  Cleans modal event handlers, and depending on the button clicked,
     * cleans the input fields and cropper artefacts and redisplays the Upload/Link buttons
     */
    _onModalHide: function() {
      // Reapply the blur effect of the background that was removed on opening the modal because
      // of conflicting with the modal-backdrop element
      $('.row.wrapper').css('backdrop-filter', 'blur(5px)');
      // remove the event handlers if existing, before applying them again next time user opens/closes modal
      // (e.g. If modal was previously opened and closed)
      // if event listeners are not removed and if user keep closing and reopning the modal, multiple event 
      // handlers will be attached to the same element, resulting in unexpected and odd behaviours
      $("#cropper-modal").off("shown.bs.modal");
      $("#cropper-modal").off("hidden.bs.modal");
      $("#cropper-output-image").attr("src", "");
      $("#preview").attr("src", "");
      // we only cear the input value if the crop was cancelled
      if (!this.applyClicked) {
        // clear file name
        this.input.val("");
        this._showOnlyButtons();
        // clear file url input
        this.field_url_input.val("");
        this.field_url_input.prop("readonly", false);
        this.field_clear.val("true");

        // destroy cropper related artefacts
        this.options.cropper.destroy();
        this.options.cropper = null;
        this.options.file = null;
        this.options.canvas=null;
      }
    },
    
    /* Show only the buttons, hiding all others
     *
     * Returns nothing.
     */
    _showOnlyButtons: function() {
      this.fields.hide();
      this.button_upload
        .add(this.field_image)
        .add(this.button_url)
        .add(this.input)
        .show();
    },

    /* Show only the URL field, hiding all others
     *
     * Returns nothing.
     */
    _showOnlyFieldUrl: function() {
      this.fields.hide();
      this.field_url.show();
    },

    /* Event listener for when a user mouseovers the hidden file input
     *
     * Returns nothing.
     */
    _onInputMouseOver: function() {
      this.button_upload.addClass('hover');
    },

    /* Event listener for when a user mouseouts the hidden file input
     *
     * Returns nothing.
     */
    _onInputMouseOut: function() {
      this.button_upload.removeClass('hover');
    },

    /* Event listener for changes in resource's name by direct input from user
     *
     * Returns nothing
     */
    _onModifyName: function() {
      this._nameIsDirty = true;
    },

    /* Event listener for when someone loses focus of URL field
     *
     * Returns nothing
     */
    _onFromWebBlur: function() {
      var url = this.field_url_input.val().match(/([^\/]+)\/?$/)
      if (url) {
        this._autoName(url.pop());
      }
    },

    /* Automatically add file name into field Name
     *
     * Select by attribute [name] to be on the safe side and allow to change field id
     * Returns nothing
     */
     _autoName: function(name) {
        if (!this._nameIsDirty){
          this.field_name.val(name);
        }
     }
  };
});
