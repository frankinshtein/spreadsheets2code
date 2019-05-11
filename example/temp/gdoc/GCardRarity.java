package com.model.gdoc;

/*
 file was automatically generated
*/

import org.jetbrains.annotations.NotNull;
import org.w3c.dom.Node;
import com.google.common.base.MoreObjects;
import java.util.*;

public class GCardRarity
{
	public static ArrayList<GCardRarity> items = new ArrayList<>();

	public static Map<String, GCardRarity> itemsMap = new HashMap<>();
    public String id;

    public int indexInArray;

    @NotNull
    public static GCardRarity get(String id){

        GCardRarity obj = getOrDefault(id, null);
        if (obj != null)
            return obj;
        throw new NoSuchElementException("not found element in GCardRarity " + id);
    }

    public static GCardRarity getOrDefault(String id, GCardRarity def){
        GCardRarity res = GLoader.utilGetItem(itemsMap, id);
        if (res != null)
            return res;
        return def;
    }

    public void init(Node node, int index, GLoader loader){
		this.id = GLoader.utilParse_String(node, "id", loader.preset);
    	indexInArray = index;
    }

    public GCardRarity(){}


    @Override
    public String toString() {
        return MoreObjects.toStringHelper(this)
                .add("id", id)
                .toString();
    }
}