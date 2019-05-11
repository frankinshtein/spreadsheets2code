package com.model.gdoc;

/*
 file was automatically generated
*/

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

    public GLoader(){
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
                        item.id = utilParse_String(child, "id", preset);
                        itemsMap.put(item.id.toLowerCase(), item);
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
                        item.id = utilParse_String(child, "id", preset);
                        itemsMap.put(item.id.toLowerCase(), item);
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
                        item.id = utilParse_String(child, "id", preset);
                        itemsMap.put(item.id.toLowerCase(), item);
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
                        item.id = utilParse_String(child, "id", preset);
                        itemsMap.put(item.id.toLowerCase(), item);
                    }
                    child = child.getNextSibling();
                }
            }

            /////////////load - GSingle
            {
                Node child = root.getElementsByTagName("single").item(0).getFirstChild();
                ArrayList<GSingle> items = listGSingle;
                items.clear();

                while(child != null)
                {
                    if (child.getNodeType() == Node.ELEMENT_NODE) {

                        GSingle item = utilGetItem(mapGSingle, utilParse_String(child, "id", preset));

                        item.init(child, items.size(), this);

                        items.add(item);
                    }
                    child = child.getNextSibling();
                }
            }
            /////////////load - GCollectionCard
            {
                Node child = root.getElementsByTagName("collection_card").item(0).getFirstChild();
                ArrayList<GCollectionCard> items = listGCollectionCard;
                items.clear();

                while(child != null)
                {
                    if (child.getNodeType() == Node.ELEMENT_NODE) {

                        GCollectionCard item = utilGetItem(mapGCollectionCard, utilParse_String(child, "id", preset));

                        item.init(child, items.size(), this);

                        items.add(item);
                    }
                    child = child.getNextSibling();
                }
            }
            /////////////load - GCollection
            {
                Node child = root.getElementsByTagName("collection").item(0).getFirstChild();
                ArrayList<GCollection> items = listGCollection;
                items.clear();

                while(child != null)
                {
                    if (child.getNodeType() == Node.ELEMENT_NODE) {

                        GCollection item = utilGetItem(mapGCollection, utilParse_String(child, "id", preset));

                        item.init(child, items.size(), this);

                        items.add(item);
                    }
                    child = child.getNextSibling();
                }
            }
            /////////////load - GCardRarity
            {
                Node child = root.getElementsByTagName("card_rarity").item(0).getFirstChild();
                ArrayList<GCardRarity> items = listGCardRarity;
                items.clear();

                while(child != null)
                {
                    if (child.getNodeType() == Node.ELEMENT_NODE) {

                        GCardRarity item = utilGetItem(mapGCardRarity, utilParse_String(child, "id", preset));

                        item.init(child, items.size(), this);

                        items.add(item);
                    }
                    child = child.getNextSibling();
                }
            }
            /////////////load - GConfig
            {
                Node child = root.getElementsByTagName("config").item(0).getFirstChild();
                ArrayList<GConfig> items = listGConfig;
                items.clear();

                while(child != null)
                {
                    if (child.getNodeType() == Node.ELEMENT_NODE) {

                        GConfig item = new GConfig();

                        item.init(child, items.size(), this);

                        items.add(item);
                    }
                    child = child.getNextSibling();
                }
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


    public static String utilParse_String(Node node, String name, String preset)
    {
        if (preset != null)
        {
            String key = name + "#" + preset;
            String value = node.getAttributes().getNamedItem(key).getNodeValue();
            if (value != null)
                return value;
        }
        String value = node.getAttributes().getNamedItem(name).getNodeValue();
        return value;
    }

    public static long utilParse_long(Node node, String name, String preset)
    {
        String value = utilParse_String(node, name, preset);
        try {
            return Long.parseLong(value);
        } catch(NumberFormatException ex) {
            return 0;
        }
    }

    public static int utilParse_int(Node node, String name, String preset)
    {
        String value = utilParse_String(node, name, preset);
        try {
            return Integer.parseInt(value);
        } catch(NumberFormatException ex) {
            return 0;
        }
    }

    public static double utilParse_double(Node node, String name, String preset)
    {
        String value = utilParse_String(node, name, preset);
        try {
            return Double.parseDouble(value);
        } catch(NumberFormatException ex) {
            return 0;
        }
    }

    public static float utilParse_float(Node node, String name, String preset)
    {
        String value = utilParse_String(node, name, preset);
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