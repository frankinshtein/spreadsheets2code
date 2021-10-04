package com.model.gdoc;

/*
 file was automatically generated
*/

import com.google.protobuf.MapEntry;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.xml.sax.SAXException;
import java.io.ByteArrayInputStream;
import java.util.*;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import java.io.IOException;
import java.util.function.Function;
import java.util.stream.Collectors;
import org.w3c.dom.NamedNodeMap;

public class GLoader
{
    public String preset;
    public Long timestamp;
    public byte[] data;


    public ArrayList<GSingle> listGSingle = new ArrayList<>();
    public Map<String, GSingle> mapGSingle = new HashMap<>();
    public ArrayList<GCollectionCard> listGCollectionCard = new ArrayList<>();
    public Map<String, GCollectionCard> mapGCollectionCard = new HashMap<>();
    public ArrayList<GCollection> listGCollection = new ArrayList<>();
    public Map<String, GCollection> mapGCollection = new HashMap<>();
    public ArrayList<GCardRarity> listGCardRarity = new ArrayList<>();
    public Map<String, GCardRarity> mapGCardRarity = new HashMap<>();
    public ArrayList<GConfig> listGConfig = new ArrayList<>();

    public Function<String, GSingle> fnString2GSingle;
    public Function<String, GCollectionCard> fnString2GCollectionCard;
    public Function<String, GCollection> fnString2GCollection;
    public Function<String, GCardRarity> fnString2GCardRarity;

    public static Function<String, Integer> fnString2int = str->{
        try {
            return Integer.parseInt(str);
        } catch (NumberFormatException ex){}
        return 0;
    };

    public static Function<String, Float> fnString2float = str->{
        try {
            return Float.parseFloat(str);
        } catch (NumberFormatException ex){}
        return 0.0f;
    };

    public static Function<String, Long> fnString2long  = str->{
        try {
            return Long.parseLong(str);
        } catch (NumberFormatException ex){}
        return 0L;
    };

    public static Function<String, String> fnString2String = str->str;




    public GLoader(){
        fnString2GSingle = str->utilGetItem(mapGSingle, str);
        fnString2GCollectionCard = str->utilGetItem(mapGCollectionCard, str);
        fnString2GCollection = str->utilGetItem(mapGCollection, str);
        fnString2GCardRarity = str->utilGetItem(mapGCardRarity, str);
    }

    public boolean load(byte[] data, String preset){
        this.data = data;
        this.preset = preset;

        try {
            DocumentBuilderFactory documentBuilderFactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder documentBuilder = documentBuilderFactory.newDocumentBuilder();
            Document document = documentBuilder.parse(new ByteArrayInputStream(data));
            Element root = document.getDocumentElement();

            timestamp = Long.parseLong(root.getAttribute("timestamp"));

            /////////////load - GSingle
            {
                Node child = root.getElementsByTagName("single").item(0).getFirstChild();

                Map<String, GSingle> itemsMap = mapGSingle;
                itemsMap.clear();

                while(child != null)
                {
                    if (child.getNodeType() == Node.ELEMENT_NODE) {
                        GSingle item = new GSingle();
                        item.id = utilParse_String_(child, "id", preset);
                        itemsMap.put(item.id.toLowerCase(), item);
                        item.xmlNode = child;
                    }
                    child = child.getNextSibling();
                }
            }
            /////////////load - GCollectionCard
            {
                Node child = root.getElementsByTagName("collection_card").item(0).getFirstChild();

                Map<String, GCollectionCard> itemsMap = mapGCollectionCard;
                itemsMap.clear();

                while(child != null)
                {
                    if (child.getNodeType() == Node.ELEMENT_NODE) {
                        GCollectionCard item = new GCollectionCard();
                        item.id = utilParse_String_(child, "id", preset);
                        itemsMap.put(item.id.toLowerCase(), item);
                        item.xmlNode = child;
                    }
                    child = child.getNextSibling();
                }
            }
            /////////////load - GCollection
            {
                Node child = root.getElementsByTagName("collection").item(0).getFirstChild();

                Map<String, GCollection> itemsMap = mapGCollection;
                itemsMap.clear();

                while(child != null)
                {
                    if (child.getNodeType() == Node.ELEMENT_NODE) {
                        GCollection item = new GCollection();
                        item.id = utilParse_String_(child, "id", preset);
                        itemsMap.put(item.id.toLowerCase(), item);
                        item.xmlNode = child;
                    }
                    child = child.getNextSibling();
                }
            }
            /////////////load - GCardRarity
            {
                Node child = root.getElementsByTagName("card_rarity").item(0).getFirstChild();

                Map<String, GCardRarity> itemsMap = mapGCardRarity;
                itemsMap.clear();

                while(child != null)
                {
                    if (child.getNodeType() == Node.ELEMENT_NODE) {
                        GCardRarity item = new GCardRarity();
                        item.id = utilParse_String_(child, "id", preset);
                        itemsMap.put(item.id.toLowerCase(), item);
                        item.xmlNode = child;
                    }
                    child = child.getNextSibling();
                }
            }

            ///init all classes

            /////////////load - GSingle
            {
                Node child = root.getElementsByTagName("single").item(0).getFirstChild();
                ArrayList<GSingle> items = listGSingle;
                items.clear();

                while(child != null)
                {
                    if (child.getNodeType() == Node.ELEMENT_NODE) {

                        Node presetNode = null;

                        String id = utilParse_String_(child, "id", preset);
                        GSingle item = utilGetItem(mapGSingle, id);

                        GSingle presetItem = utilGetItem(mapGSingle, id + "#" + preset);
                        if (presetItem != null)
                            presetNode = presetItem.xmlNode;
                        item.init(child, presetNode, items.size(), this);
                        items.add(item);
                    }
                    child = child.getNextSibling();
                }

                /*
                for (GSingle presetItem:items){
                    String end =  "#"+preset;
                    if (presetItem.id.endsWith(end)){
                        GSingle mainItem = utilGetItem(mapGSingle, presetItem.id.substring(0, presetItem.id.length() - end.length()));

                        if (presetItem.has_id)
                            mainItem.id = presetItem.id;
                        if (presetItem.has_value)
                            mainItem.value = presetItem.value;
                        if (presetItem.has_level)
                            mainItem.level = presetItem.level;
                        if (presetItem.has_test)
                            mainItem.test = presetItem.test;
                    }
                }
                */
            }
            /////////////load - GCollectionCard
            {
                Node child = root.getElementsByTagName("collection_card").item(0).getFirstChild();
                ArrayList<GCollectionCard> items = listGCollectionCard;
                items.clear();

                while(child != null)
                {
                    if (child.getNodeType() == Node.ELEMENT_NODE) {

                        Node presetNode = null;

                        String id = utilParse_String_(child, "id", preset);
                        GCollectionCard item = utilGetItem(mapGCollectionCard, id);

                        GCollectionCard presetItem = utilGetItem(mapGCollectionCard, id + "#" + preset);
                        if (presetItem != null)
                            presetNode = presetItem.xmlNode;
                        item.init(child, presetNode, items.size(), this);
                        items.add(item);
                    }
                    child = child.getNextSibling();
                }

                /*
                for (GCollectionCard presetItem:items){
                    String end =  "#"+preset;
                    if (presetItem.id.endsWith(end)){
                        GCollectionCard mainItem = utilGetItem(mapGCollectionCard, presetItem.id.substring(0, presetItem.id.length() - end.length()));

                        if (presetItem.has_id)
                            mainItem.id = presetItem.id;
                        if (presetItem.has_collection)
                            mainItem.collection = presetItem.collection;
                        if (presetItem.has_rarity)
                            mainItem.rarity = presetItem.rarity;
                    }
                }
                */
            }
            /////////////load - GCollection
            {
                Node child = root.getElementsByTagName("collection").item(0).getFirstChild();
                ArrayList<GCollection> items = listGCollection;
                items.clear();

                while(child != null)
                {
                    if (child.getNodeType() == Node.ELEMENT_NODE) {

                        Node presetNode = null;

                        String id = utilParse_String_(child, "id", preset);
                        GCollection item = utilGetItem(mapGCollection, id);

                        GCollection presetItem = utilGetItem(mapGCollection, id + "#" + preset);
                        if (presetItem != null)
                            presetNode = presetItem.xmlNode;
                        item.init(child, presetNode, items.size(), this);
                        items.add(item);
                    }
                    child = child.getNextSibling();
                }

                /*
                for (GCollection presetItem:items){
                    String end =  "#"+preset;
                    if (presetItem.id.endsWith(end)){
                        GCollection mainItem = utilGetItem(mapGCollection, presetItem.id.substring(0, presetItem.id.length() - end.length()));

                        if (presetItem.has_id)
                            mainItem.id = presetItem.id;
                        if (presetItem.has_level)
                            mainItem.level = presetItem.level;
                    }
                }
                */
            }
            /////////////load - GCardRarity
            {
                Node child = root.getElementsByTagName("card_rarity").item(0).getFirstChild();
                ArrayList<GCardRarity> items = listGCardRarity;
                items.clear();

                while(child != null)
                {
                    if (child.getNodeType() == Node.ELEMENT_NODE) {

                        Node presetNode = null;

                        String id = utilParse_String_(child, "id", preset);
                        GCardRarity item = utilGetItem(mapGCardRarity, id);

                        GCardRarity presetItem = utilGetItem(mapGCardRarity, id + "#" + preset);
                        if (presetItem != null)
                            presetNode = presetItem.xmlNode;
                        item.init(child, presetNode, items.size(), this);
                        items.add(item);
                    }
                    child = child.getNextSibling();
                }

                /*
                for (GCardRarity presetItem:items){
                    String end =  "#"+preset;
                    if (presetItem.id.endsWith(end)){
                        GCardRarity mainItem = utilGetItem(mapGCardRarity, presetItem.id.substring(0, presetItem.id.length() - end.length()));

                        if (presetItem.has_id)
                            mainItem.id = presetItem.id;
                    }
                }
                */
            }
            /////////////load - GConfig
            {
                Node child = root.getElementsByTagName("config").item(0).getFirstChild();
                ArrayList<GConfig> items = listGConfig;
                items.clear();

                while(child != null)
                {
                    if (child.getNodeType() == Node.ELEMENT_NODE) {

                        Node presetNode = null;

                        GConfig item = new GConfig();
                        item.xmlNode = child;
                        item.init(child, presetNode, items.size(), this);
                        items.add(item);
                    }
                    child = child.getNextSibling();
                }

                /*
                */
            }

            return true;
        } catch (ParserConfigurationException ex)
        {}
        catch (SAXException ex)
        {}
        catch (IOException ex)
        {}

        return false;
    }


    public void assignStaticInstances(){
        GSingle.items = listGSingle;
        GSingle.itemsMap = mapGSingle;
        GCollectionCard.items = listGCollectionCard;
        GCollectionCard.itemsMap = mapGCollectionCard;
        GCollection.items = listGCollection;
        GCollection.itemsMap = mapGCollection;
        GCardRarity.items = listGCardRarity;
        GCardRarity.itemsMap = mapGCardRarity;
        GConfig.items = listGConfig;
    }



    private static <T> List<T> utilParse_String2List(String st, Function<String, T> fn)
    {
        return Arrays.stream(st.split(",")).map(String::trim).map(fn).collect(Collectors.toList());
    }

    public static <T> T utilParse_Single(Node node, String name, String preset, Node presetNode, Function<String, T> fn)
    {
        String st = utilParse_String(node, name, preset, presetNode);
        return fn.apply(st);
    }

    static <T> List<T> utilParse_List(Node node, String name, String preset, Node presetNode, Function<String, T> fn)
    {
        return utilParse_String2List(utilParse_String(node, name, preset, presetNode), fn);
    }

    static <T> Map<String, T> utilParse_Named(Node node, String name, String preset, Node presetNode, Function<String, T> fn){

        NamedNodeMap attrs = node.getAttributes();
        String pref = name + ".";


        String suffix = "#" + preset;

        Map<String, T> items = new HashMap<>();
        for (int i = 0; i < attrs.getLength(); ++i)
        {
            Node attrNode = attrs.item(i);
            String attrName = attrNode.getNodeName();

            if (!attrName.startsWith(pref) || attrName.contains("#"))
                continue;

            String nam = attrName.substring(pref.length());
            String value = attrNode.getNodeValue();

            if (preset != null){
                Node nodePreset = attrs.getNamedItem(attrName + suffix);
                if (nodePreset != null)
                    value = nodePreset.getNodeValue();
            }

            items.put(nam, fn.apply(value));

        }

        return items;
    }

    static <T> Map<String, List<T>> utilParse_NamedList(Node node, String name, String preset, Node presetNode, Function<String, T> fn){
        Map<String, String> rs = utilParse_Named(node, name, preset, presetNode, fnString2String);
        return rs.entrySet().stream().collect(Collectors.toMap(entry->entry.getKey(), entry->utilParse_String2List(entry.getValue(), fn)));
    }

    private static String utilParse_String(Node node, String name, String preset, Node presetNode)
    {
        String ret = null;
        if (presetNode != null)
            ret = utilParse_String_(presetNode, name, preset);
        if (ret != null && ret.length() > 0)
            return ret;
        return utilParse_String_(node, name, preset);
    }

    private static String utilParse_String_(Node node, String name, String preset)
    {
        if (preset != null)
        {
            String key = name + "#" + preset;
            Node attr = node.getAttributes().getNamedItem(key);
            if (attr != null){
                String value = attr.getNodeValue();
                return value;
            }

        }
        String value = node.getAttributes().getNamedItem(name).getNodeValue();
        return value;
    }

    public static <T> T utilGetItem(Map<String, T> itemsMap, String name)
    {
        name = name.toLowerCase();
        return itemsMap.getOrDefault(name, null);
    }
}