package com.model.gdoc;

/*
 file was automatically generated
*/

import org.jetbrains.annotations.NotNull;
import org.w3c.dom.Node;
import com.google.common.base.MoreObjects;
import java.util.*;

public class GSingle
{
	public static ArrayList<GSingle> items = new ArrayList<>();

	public static Map<String, GSingle> itemsMap = new HashMap<>();
    public String id;
    public List<Integer> value;
    public Map<String, Integer> level;
    public Map<String, List<String>> test;

    public int indexInArray;
    public Node xmlNode;

    @NotNull
    public static GSingle get(String id){

        GSingle obj = getOrDefault(id, null);
        if (obj != null)
            return obj;
        throw new NoSuchElementException("not found element in GSingle " + id);
    }

    public static GSingle getOrDefault(String id, GSingle def){
        GSingle res = GLoader.utilGetItem(itemsMap, id);
        if (res != null)
            return res;
        return def;
    }

    public void init(Node node, Node presetNode, int index, GLoader loader){

        this.value = GLoader.utilParse_List(node, "value", loader.preset, presetNode, loader.fnString2int);
        this.level = GLoader.utilParse_Named(node, "level", loader.preset, presetNode, loader.fnString2int);
        this.test = GLoader.utilParse_NamedList(node, "test", loader.preset, presetNode, loader.fnString2String);
    	indexInArray = index;
    }

    public GSingle(){}


    @Override
    public String toString() {
        return MoreObjects.toStringHelper(this)
                .add("id", id)
                .add("value", value)
                .add("level", level)
                .add("test", test)
                .toString();
    }
}