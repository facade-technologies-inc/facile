API Reference
=============

This page contains auto-generated API reference documentation

.. toctree::

    {% for page in pages %}
        {% if page.top_level_object and page.display %}
            {% set name = page.include_path.split("/")[-2] %}
            {% if "ui_" not in name %}
                {{ name }} <{{ page.include_path }}>
            {% endif %}
        {% endif %}
    {% endfor %}

