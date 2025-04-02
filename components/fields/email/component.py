from django_components import Component, register


@register("email_field")
class PasswordField(Component):
    template_name = "fields/email/template.html"

    def get_context_data(
        self,
        field,
        icon="lucide--mail",
        placeholder="Email Address",
        field_id="id_login",
    ):

        field.field.widget.attrs.update(
            {
                "placeholder": placeholder,
                "id": field_id,
            }
        )

        return {
            "field": field,
            "icon": icon,
            "placeholder": placeholder,
        }


# {% component "email_field" field=form.login field_id="id_login" / %}
