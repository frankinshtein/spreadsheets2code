package com.model.gdoc;

/*
 file was automatically generated
*/

import org.jetbrains.annotations.NotNull;
import org.w3c.dom.Node;
import com.google.common.base.MoreObjects;
import java.util.*;

public class GCollectionCard
{
	public static ArrayList<GCollectionCard> items = new ArrayList<>();

	public static Map<String, GCollectionCard> itemsMap = new HashMap<>();
    public String id;
    public GCollection collection;
    public GCardRarity rarity;

    public int indexInArray;
    public Node xmlNode;

    @NotNull
    public static GCollectionCard get(String id){

        GCollectionCard obj = getOrDefault(id, null);
        if (obj != null)
            return obj;
        throw new NoSuchElementException("not found element in GCollectionCard " + id);
    }

    public static GCollectionCard getOrDefault(String id, GCollectionCard def){
        GCollectionCard res = GLoader.utilGetItem(itemsMap, id);
        if (res != null)
            return res;
        return def;
    }

    public void init(Node node, Node presetNode, int index, GLoader loader){

		this.collection = GLoader.utilParse_Single(node, "collection", loader.preset, presetNode, loader.fnString2GCollection);
		this.rarity = GLoader.utilParse_Single(node, "rarity", loader.preset, presetNode, loader.fnString2GCardRarity);
    	indexInArray = index;
    }

    public GCollectionCard(){}


    @Override
    public String toString() {
        return MoreObjects.toStringHelper(this)
                .add("id", id)
                .add("collection", collection)
                .add("rarity", rarity)
                .toString();
    }
}