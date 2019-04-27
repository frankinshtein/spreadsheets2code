package {{args.package}};

/*
 file was automatically generated
*/

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.xml.sax.SAXException;

import java.util.*;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import java.io.IOException;
import java.io.InputStream;

public class {{loader}}
{
    public {{loader}}(InputStream stream){

        try {
            DocumentBuilderFactory documentBuilderFactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder documentBuilder = documentBuilderFactory.newDocumentBuilder();
            Document document = documentBuilder.parse(stream);
            Element root = document.getDocumentElement();


            {% for cls in classes_with_id %}
            /////////////load - {{cls.nice_name}}
            {
                Node child = root.getElementsByTagName("{{cls.name}}").item(0).getFirstChild();

                Map<String, {{cls.nice_name}}> itemsMap = new HashMap<>();
                while(child != null)
                {
                    if (child.getNodeType() == Node.ELEMENT_NODE) {

                        {{cls.nice_name}} item = new {{cls.nice_name}}();
                        item.id = utilParse_String(child, "id");
                        itemsMap.put(item.id.toLowerCase(), item);
                    }
                    child = child.getNextSibling();
                }

                {{cls.nice_name}}.itemsMap = itemsMap;
            }
            {% endfor %}

            {% for cls in classes %}
            /////////////load - {{cls.nice_name}}
            {
                Node child = root.getElementsByTagName("{{cls.name}}").item(0).getFirstChild();
                ArrayList<{{cls.nice_name}}> items = new ArrayList<>();
                Map<String, {{cls.nice_name}}> itemsMap = new HashMap<>();
                while(child != null)
                {
                    if (child.getNodeType() == Node.ELEMENT_NODE) {

                        {% if cls.has_id %}
                        {{cls.nice_name}} item = {{cls.nice_name}}.get(utilParse_String(child, "id"));
                        {% else %}
                        {{cls.nice_name}} item = new {{cls.nice_name}}();
                        {% endif %}

                        item.init(child, items.size());

                        items.add(item);
                    }
                    child = child.getNextSibling();
                }

                {{cls.nice_name}}.items = items;
            }
            {% endfor %}
        } catch (ParserConfigurationException ex)
        {}
        catch (SAXException ex)
        {}
        catch (IOException ex)
        {}
    }


    public static String utilParse_String(Node node, String name)
    {
        String value = node.getAttributes().getNamedItem(name).getNodeValue();
        return value;
    }

    public static int utilParse_int(Node node, String name)
    {
        String value = node.getAttributes().getNamedItem(name).getNodeValue();
        try {
            return Integer.parseInt(value);
        } catch(NumberFormatException ex) {
            return 0;
        }
    }

    public static double utilParse_double(Node node, String name)
    {
        String value = node.getAttributes().getNamedItem(name).getNodeValue();
        try {
            return Double.parseDouble(value);
        } catch(NumberFormatException ex) {
            return 0;
        }
    }

    public static float utilParse_float(Node node, String name)
    {
        String value = node.getAttributes().getNamedItem(name).getNodeValue();
        try {
            return Float.parseFloat(value);
        } catch(NumberFormatException ex) {
            return 0;
        }
    }

    public static <T> T utilGetItem(Map<String, T> itemsMap, String name)
    {
        name = name.toLowerCase();
        return itemsMap.getOrDefault(name, null);
    }
}