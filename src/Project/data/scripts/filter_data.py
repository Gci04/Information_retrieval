import numpy as np
import pickle, os, sys

def main(data_folder='../'):
    """Joins data retrieved documents by removing any exixting duplicates
    :param data_folder : string, path to directory containing data files
    :return : None
    """
    data_filenames = []
    for (_,_,filenames) in os.walk(data_folder):
        data_filenames.extend([i for i in filenames if i.endswith('.pickle')])
        break

    full_data = np.zeros((1,2))
    for file in data_filenames:
        with open(os.path.join(data_folder,file),'rb') as handle:
            full_data = np.vstack((full_data,pickle.load(handle)))

    # filter out duplicates
    titles = []
    res_idx = []
    for i, (_,article) in enumerate(full_data[1:],1):
        title = article['title'].lower()
        if title not in titles :
            titles.append(title)
            res_idx.append(i)

    # save filtered data to disk
    with open(os.path.join(data_folder,'raw_data_filtered.pickle'),'wb') as handle:
        pickle.dump(full_data[res_idx],handle,protocol=pickle.HIGHEST_PROTOCOL)

    # delete old data from disk
    for file in data_filenames:
        if file.endswith('.pickle') and file != 'raw_data_filtered.pickle':
            os.system(f'rm {os.path.join(data_folder,file)}')

if __name__ == '__main__':
    main()
