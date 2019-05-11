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

    public void init(Node node, int index, GLoader loader){
		this.id = GLoader.utilParse_String(node, "id", loader.preset);
		this.level = GLoader.utilParse_int(node, "level", loader.preset);
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