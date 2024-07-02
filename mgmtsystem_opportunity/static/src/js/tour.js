// odoo.define('mgmtsystem_opportunity.tour', function(require) {
//     "use strict";
    
//     var core = require('web.core');
//     var tour = require('web_tour.tour');
    
//     var _t = core._t;

//     tour.register('mgmtsystem_opportunity_tour', {
//         url: "/web",
//     }, [tour.STEPS.MENU_MORE, {
//         trigger: '.o_app[data-menu-xmlid="mgmtsystem_opportunity.menu_opportunity_root"], .oe_menu_toggler[data-menu-xmlid="mgmtsystem_opportunity.menu_opportunity_root"]',
//         content: _t('Registre y gestione sus matrices de <b>riesgos y oportunidades.</b> <i>Empiece aquí.</i>'),
//         position: 'bottom',
//     }, {
//         trigger: ".o_list_button_add",
//         extra_trigger: ".o_matrix_block",
//         content: _t("Comenzará creando <b>fuentes con lineas de riesgo</b>"),
//         position: "right",
//     }, {
//         trigger: ".o_required_modifier input",
//         extra_trigger: ".o_matrix_block",
//         content: _t("Una <b>fuente</b> puede ser un proceso u algún documento."),
//         position: "top",
//     }, {
//         trigger: ".o_field_x2many_list_row_add > a",
//         extra_trigger: ".o_matrix_block",
//         content: _t("<b>Añada riesgos</b> presionando en 'Añadir un elemento'"),
//         position: "bottom",
//     }, {
//         trigger: ".o_mbline_name",
//         extra_trigger: ".o_matrix_block",
//         content: _t("<b>Defina el riesgo encontrado,</b> por ejemplo: Sub-estimación de costos"),
//         position: "bottom",
//     }, {
//         trigger: ".o_mbline_department_id",
//         extra_trigger: ".o_matrix_block",
//         content: _t("<b>Opcional:</b> Si la fuente fue alguna área elegirla aquí"),
//         position: "top",
//     }, {
//         trigger: ".o_mbline_effect",
//         extra_trigger: ".o_matrix_block",
//         content: _t("<b>Defina efectos.</b> ¿Qué consecuencias tiene este riesgo?"),
//         position: "right",
//     }, {
//         trigger: ".o_mbline_cause",
//         extra_trigger: ".o_matrix_block",
//         content: _t("<b>Defina las causas.</b> ¿Cuál es el origen de este riesgo?"),
//         position: "right",
//     }, {
//         trigger: ".o_mbline_evaluation_id",
//         extra_trigger: ".o_matrix_block",
//         content: _t("<b>Elija el tipo de evaluación,</b> se llenarán automaticamente los índices para calificar"),
//         position: "top",
//     }, {
//         trigger: ".o_mbline_result_ids",
//         extra_trigger: ".o_matrix_block",
//         content: _t("Aquí se refleja los resultados, <b>presiona sobre el cuadro</b> para empezar a calificar"),
//         position: "right",
//     }, {
//         trigger: ".o_mbline_result_ids .o_external_button",
//         extra_trigger: ".o_matrix_block",
//         content: _t("<b>Verifica los criterios</b> con que se va a evaluar el riesgo"),
//         position: "right",
//     }, {
//         trigger: ".o_mbline_result_ids .o_field_number",
//         extra_trigger: ".o_matrix_block",
//         content: _t("Evalua el riesgo colocando un número según se piense"),
//         position: "right",
//     }
//     ]);

//     });