package {{args.package}};

/*
 file was automatically generated
*/

import org.jetbrains.annotations.NotNull;
import org.w3c.dom.Node;
import com.google.common.base.MoreObjects;
import java.util.*;

public class {{cls.nice_name}}
{
	public static ArrayList<{{cls.nice_name}}> items = new ArrayList<>();

	{% if cls.has_id %}
	public static Map<String, {{cls.nice_name}}> itemsMap = new HashMap<>();
    {% endif %}
    {% for field in cls.fields %}
    public {{ field.type.nice_name }} {{ field.nice_name}};
    {% endfor %}

    public int indexInArray;

    {% if cls.has_id %}
    @NotNull
    public static {{cls.nice_name}} get(String id){

        {{cls.nice_name}} obj = getOrDefault(id, null);
        if (obj != null)
            return obj;
        throw new NoSuchElementException("not found element in {{cls.nice_name}} " + id);
    }

    public static {{cls.nice_name}} getOrDefault(String id, {{cls.nice_name}} def){
        {{cls.nice_name}} res = {{loader}}.utilGetItem(itemsMap, id);
        if (res != null)
            return res;
        return def;
    }
    {% endif %}

    public void init(Node node, int index){
		{% for field in cls.fields %}
		{% if field.type.custom %}
		this.{{field.nice_name}} =  {{field.type.nice_name}}.get({{loader}}.utilParse_String(node, "{{field.name}}"));
		{% else  %}
		this.{{field.nice_name}} = {{loader}}.utilParse_{{field.type.name}}(node, "{{field.name}}");
    	{% endif %}
    	{% endfor %}
    	indexInArray = index;
    }

    public {{cls.nice_name}}(){}


    @Override
    public String toString() {
        return MoreObjects.toStringHelper(this)
        {% for field in cls.fields %}
                .add("{{field.nice_name}}", {{field.nice_name}})
        {% endfor %}
                .toString();
    }
}