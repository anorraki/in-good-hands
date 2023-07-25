document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;

            console.log(page);
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            // this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // TODO: get data from inputs and show them in summary

/*
            function getCheckboxValues() {
                const markedCheckbox = document.querySelectorAll('input[name=categories]:checked');
                let checkboxValues = [];
                markedCheckbox.forEach(function (box) {
                    checkboxValues.push(box.value);
                });
                return checkboxValues;
            }
*/

/*
            function getChosenCategories(event) {
                let arr = getCheckboxValues();
                let myUrl = '/get_categories?';
                let params = new URLSearchParams();
                arr.forEach(function (id) {
                    params.append('category_id', id);
                });
                let parameters = params.toString();
                myUrl = myUrl + parameters;
                console.log(myUrl);
                const test = document.querySelector('#summary-categories');
                fetch(myUrl)
                    .then(response => response.json())
                    .then(data => {
                        while (test.firstChild) {
                            test.removeChild(test.lastChild);
                        }
                        data.forEach(function (element) {

                        });
                    });
            }
*/

            if (this.currentStep === 4) {
                const summaryBtn = document.querySelector('#summary-btn');
                const summaryBags = document.querySelector('#summary-bags');
                const summaryCategories = document.querySelector('#summary-categories');
                const summaryOrganization = document.querySelector('#summary-organization');
                const summaryAddress = document.querySelector('#summary-address');
                const summaryCity = document.querySelector('#summary-city');
                const summaryPostCode = document.querySelector('#summary-postcode');
                const summaryPhone = document.querySelector('#summary-phone');
                const summaryDate = document.querySelector('#summary-date');
                const summaryTime = document.querySelector('#summary-time');
                const summaryMoreInfo = document.querySelector('#summary-more-info');

                summaryBtn.addEventListener('click', function () {
                    let bags = document.querySelector("input[name=bags]").value;
                    summaryBags.innerHTML = "Worków: " + bags + ". Przekazujesz\u00A0";

                    let catValues = [];
                    checkboxes.forEach(function (checkbox) {
                        let catSpanText = checkbox.parentNode.querySelector('.description').innerHTML;
                        if (checkbox.checked) {
                            catValues.push(catSpanText);
                        }
                    });
                    summaryCategories.innerHTML = catValues.join(', ');

                    const radioOrg = document.querySelector('input[name=organization]:checked');
                    let orgName = radioOrg.parentNode.querySelector('.title').innerHTML;
                    summaryOrganization.innerHTML = "Dla organizacji " + orgName;

                    summaryAddress.innerHTML = document.querySelector("input[name=address]").value;
                    summaryCity.innerHTML = document.querySelector("input[name=city]").value;
                    summaryPostCode.innerHTML = document.querySelector("input[name=postcode]").value;
                    summaryPhone.innerHTML = document.querySelector("input[name=phone]").value;
                    summaryDate.innerHTML = document.querySelector("input[name=date]").value;
                    summaryTime.innerHTML = document.querySelector("input[name=time]").value;
                    summaryMoreInfo.innerHTML = document.querySelector("textarea[name=more_info]").value;
                });
            }
        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */

        /** Validation Step 1. Check at least 1 checkbox
        */


        submit(e) {
            //e.preventDefault();
            this.currentStep++;
            this.updateForm();
        }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }

    const checkboxes = document.querySelectorAll("input[name=categories]");
    const institutions = document.querySelectorAll(".institutions");

    let chosenCat = [];

    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            if (this.checked) {
                chosenCat.push(this.value);
            } else {
                let index = chosenCat.indexOf(this.value);
                chosenCat.splice(index, 1);
            }
            institutions.forEach(function (institution) {
                let institutionCat = institution.dataset.value;
                let institutionCatArray = institutionCat.split(' ');
                const containsCategories = chosenCat.every(function (category) {
                    return institutionCatArray.includes(category);
                });
                if (containsCategories === false || chosenCat.length === 0) {
                    institution.setAttribute("hidden", "");
                } else {
                    institution.removeAttribute("hidden");
                }
            });

            const orgRadios = document.querySelectorAll('input[name=organization]');
            orgRadios.forEach(function (radio) {
                radio.checked = false;
            });
        });
    });
});