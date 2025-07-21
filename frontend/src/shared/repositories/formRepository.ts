
export interface FormResponse {
    success: boolean;
    message: string;
}

export interface FormRepository {
    validate: (disableCheckValidate?: boolean)=> FormResponse;
}

export interface FormProps {
    disabled?: boolean;
}