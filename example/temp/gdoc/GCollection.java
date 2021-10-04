package com.model.gdoc;

/*
 file was automatically generated
*/

import org.jetbrains.annotations.NotNull;
import org.w3c.dom.Node;
import com.google.common.base.MoreObjects;
import java.util.*;

public class GCollection
{
	public static ArrayList<GCollection> items = new ArrayList<>();

	public static Map<String, GCollection> itemsMap = new HashMap<>();
    public String id;
    public int level;

    public int indexInArray;
    public Node xmlNode;

    @NotNull
    public static GCollection get(String id){

        GCollection obj = getOrDefault(id, null);
        if (obj != null)
            return obj;
        throw new NoSuchElementException("not found element in GCollection " + id);
    }

    public static GCollection getOrDefault(String id, GCollection def){
        GCollection res = GLoader.utilGetItem(itemsMap, id);
        if (res != null)
            return res;
        return def;
    }

    public void init(Node node, Node presetNode, int index, GLoader loader){

		this.level = GLoader.utilParse_Single(node, "level", loader.preset, presetNode, loader.fnString2int);
    	indexInArray = index;
    }

    public GCollection(){}


    @Override
    public String toString() {
        return MoreObjects.toStringHelper(this)
                .add("id", id)
                .add("level", level)
                .toString();
    }
}