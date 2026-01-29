import React, { createContext, useContext, useState, ReactNode } from "react";
import CustomModal, {ModalHandles} from "../components/Modal";
import AuthorizeMultipleOci from "../components/AuthorizeMultipleOci";
import { useGlobalComponents } from "./GlobalUIContext";


interface AutorizeMultiplesApacContextType {
  selected: number[];
  isSelected: (id: number) => boolean;
  toggleOne: (id: number) => void;
  toggleAll: (ids: number[]) => void;
  length: ()=> number;
  openModalAuthorization: () => void;
  removeOne: (id: number) => void;
  clearSelection: () => void;
}

const AutorizeMultiplesApacContext = createContext<AutorizeMultiplesApacContextType | null>(null);

export function useAutorizeMultiplesApac() {
  const context = useContext(AutorizeMultiplesApacContext);
  if (!context) {
    throw new Error("useAutorizeMultiplesApac deve ser usado dentro do Provider");
  }
  return context;
}

interface AutorizeProps {
  children: ReactNode;
}

export default function AutorizeMultiplesApacProvider({ children }: AutorizeProps) {
  const [selected, setSelected] = useState<number[]>([]);
  const modalRef = React.useRef<ModalHandles>(null);
  const { showAlert } = useGlobalComponents();
  const MAX_SELECTION = 50;


  const isSelected = (id: number) => selected.includes(id);

    const toggleOne = (id: number) => {
      setSelected((prev) => {
        // Se já está selecionado → pode remover normal
        if (prev.includes(id)) {
          return prev.filter((item) => item !== id);
        }

        // Se vai adicionar → validar limite
        if (prev.length >= MAX_SELECTION) {
          showAlert({color: "error", message: "Limite máximo de 50 OCIs selecionadas"});
          return prev;
        }

        return [...prev, id];
      });
    };

  const toggleAll = (ids: number[]) => {
    setSelected((prev) => {
      const allSelected = ids.every((id) => prev.includes(id));

      // Se todos já estão selecionados → remover
      if (allSelected) {
        return prev.filter((id) => !ids.includes(id));
      }

      // IDs que ainda não estão selecionados
      const newIds = ids.filter((id) => !prev.includes(id));

      // Espaço restante até o limite
      const remainingSlots = MAX_SELECTION - prev.length;

      // Se não há mais espaço
      if (remainingSlots <= 0) {
          showAlert({color: "error", message: "Limite máximo de 50 OCIs selecionadas"});
        return prev;
      }

      // Pega só a quantidade permitida
      const idsToAdd = newIds.slice(0, remainingSlots);

      // Se nem todos puderam ser adicionados → alerta
      if (idsToAdd.length < newIds.length) {
        showAlert({color: "error", message: "Limite máximo de 50 OCIs selecionadas"});
      }

      return [...prev, ...idsToAdd];
    });
  };

  const clearSelection = () => setSelected([]);

  const length = () => selected.length;

  const openModalAuthorization = () => modalRef.current?.openModal();

  const removeOne = (id: number) => {
      setSelected(prev => prev.filter(item => item !== id));
  };
  



  return (
    <AutorizeMultiplesApacContext.Provider
      value={{
        selected,
        isSelected,
        toggleOne,
        toggleAll,
        clearSelection,
        length,
        removeOne,
        openModalAuthorization
      }}
    >
      {children}
        <CustomModal ref={modalRef} title="Autorizar Multiplas OCI'S">
          <AuthorizeMultipleOci/>
        </CustomModal>
    </AutorizeMultiplesApacContext.Provider>
  );
}
