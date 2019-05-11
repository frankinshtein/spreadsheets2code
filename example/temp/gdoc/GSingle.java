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
    public List<Tuple<String, int>> level;
    public List<int> value;
    public List<Tuple<String, List<String>>> test;
    public String id;

    public int indexInArray;

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

    public void init(Node node, int index, GLoader loader){
		this.level = GLoader.utilParse_NamedList<int>(node, "level", loader.preset);
		this.value = GLoader.utilParse_int(node, "value", loader.preset);
		this.test = GLoader.utilParse_NamedList< List<String> >(node, "test", loader.preset);
		this.id = GLoader.utilParse_String(node, "id", loader.preset);
    	indexInArray = index;
    }

    public GSingle(){}


    @Override
    public String toString() {
        return MoreObjects.toStringHelper(this)
                .add("level", level)
                .add("value", value)
                .add("test", test)
                .add("id", id)
                .toString();
    }
}